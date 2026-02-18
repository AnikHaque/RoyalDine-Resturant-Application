from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.contrib.auth.models import User
from django.db.models import Count, Q
from orders.models import Order # আপনার অর্ডারের মডেলটি ইমপোর্ট করুন
from django.http import HttpResponseForbidden

@login_required
def inbox(request):
    user = request.user
    # ইউজার যেসব চ্যাটে যুক্ত আছে
    conversations = Conversation.objects.filter(participants=user).order_by('-updated_at')
    
    # --- প্রফেশনাল ইউজার ফিল্টারিং লজিক ---
    users_to_chat = User.objects.none()

    # ১. অ্যাডমিন বা স্টাফ হলে সবার লিস্ট দেখতে পারবে
    if user.is_staff or user.is_superuser:
        users_to_chat = User.objects.exclude(id=user.id)
@login_required
def inbox(request):
    user = request.user
    conversations = Conversation.objects.filter(participants=user).order_by('-updated_at')
    
    users_to_chat = User.objects.none()

    # ১. অ্যাডমিন বা স্টাফ
    if user.is_staff or user.is_superuser:
        users_to_chat = User.objects.exclude(id=user.id)

    # ২. ডেলিভারি ম্যান (আপনার অর্ডারে ফিল্ডের নাম 'user' এবং 'delivery_man')
    elif user.groups.filter(name='Delivery Man').exists():
        admins_staff = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
        # এখানে 'user' ই হলো কাস্টমার
        customer_ids = Order.objects.filter(delivery_man=user).values_list('user_id', flat=True)
        customers = User.objects.filter(id__in=customer_ids)
        users_to_chat = (admins_staff | customers).distinct()

    # ৩. সাধারণ কাস্টমার
    else:
        admins_staff = User.objects.filter(Q(is_staff=True) | Q(is_superuser=True))
        # আপনার অর্ডারের ফিল্ড চেক করে 'user' ব্যবহার করা হয়েছে
        delivery_man_ids = Order.objects.filter(user=user, delivery_man__isnull=False).values_list('delivery_man_id', flat=True)
        delivery_men = User.objects.filter(id__in=delivery_man_ids)
        users_to_chat = (admins_staff | delivery_men).distinct()

    return render(request, 'chat/inbox.html', {
        'conversations': conversations, 
        'all_users': users_to_chat
    })

@login_required
def chat_detail(request, convo_id):
    # ইউজার কি এই কনভারসেশনের পার্টিসিপেন্ট? না হলে ৪-৪ এরর
    conversation = get_object_or_404(Conversation, id=convo_id, participants=request.user)
    messages = conversation.messages.all()
    
    # মেসেজ রিড মার্ক করা
    conversation.messages.exclude(sender=request.user).update(is_read=True)

    if request.method == "POST":
        text = request.POST.get('message')
        if text:
            Message.objects.create(conversation=conversation, sender=request.user, text=text)
            conversation.save() 
            return redirect('chat_detail', convo_id=convo_id)

    return render(request, 'chat/chat_room.html', {'conversation': conversation, 'messages': messages})


@login_required
def start_chat(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    user = request.user

    # --- সিকিউরিটি চেক: সে কি এই ইউজারের সাথে চ্যাট শুরু করতে পারবে? ---
    if not user.is_staff and not user.is_superuser:
        
        # ১. ডেলিভারি ম্যান যদি চ্যাট শুরু করতে চায়
        if user.groups.filter(name='Delivery Man').exists():
            # চেক করবে এই target_user কি তার কোনো অর্ডারের কাস্টমার (user)?
            is_valid_customer = Order.objects.filter(delivery_man=user, user=target_user).exists()
            if not (target_user.is_staff or is_valid_customer):
                return HttpResponseForbidden("আপনি শুধুমাত্র আপনার কাস্টমার বা স্টাফদের সাথে চ্যাট করতে পারেন।")
        
        # ২. সাধারণ কাস্টমার যদি চ্যাট শুরু করতে চায়
        else:
            # চেক করবে এই target_user কি তার কোনো অর্ডারের ডেলিভারি ম্যান (delivery_man)?
            is_valid_delivery_man = Order.objects.filter(user=user, delivery_man=target_user).exists()
            if not (target_user.is_staff or is_valid_delivery_man):
                return HttpResponseForbidden("আপনি শুধুমাত্র স্টাফ বা আপনার ডেলিভারি পার্টনারের সাথে চ্যাট করতে পারেন।")

    # আগে থেকে দুজনের মধ্যে চ্যাট আছে কি না চেক
    convo = Conversation.objects.annotate(n=Count('participants')).filter(
        n=2, 
        participants=request.user
    ).filter(participants=target_user).first()

    if not convo:
        convo = Conversation.objects.create()
        convo.participants.add(request.user, target_user)
    
    return redirect('chat_detail', convo_id=convo.id)