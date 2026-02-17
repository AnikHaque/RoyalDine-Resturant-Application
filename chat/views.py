from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message
from django.contrib.auth.models import User
from django.db.models import Count

@login_required
def inbox(request):
    # ইউজার যেসব চ্যাটে যুক্ত আছে
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')
    # সব ইউজার (নতুন মেসেজ পাঠানোর জন্য)
    all_users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/inbox.html', {'conversations': conversations, 'all_users': all_users})

@login_required
def chat_detail(request, convo_id):
    conversation = get_object_or_404(Conversation, id=convo_id, participants=request.user)
    messages = conversation.messages.all()
    
    # অন্যের পাঠানো মেসেজগুলো 'Read' মার্ক করা
    conversation.messages.exclude(sender=request.user).update(is_read=True)

    if request.method == "POST":
        text = request.POST.get('message')
        if text:
            Message.objects.create(conversation=conversation, sender=request.user, text=text)
            conversation.save() # updated_at টাইম চেঞ্জ হবে
            return redirect('chat_detail', convo_id=convo_id)

    return render(request, 'chat/chat_room.html', {'conversation': conversation, 'messages': messages})

@login_required
def start_chat(request, user_id):
    target_user = get_object_or_404(User, id=user_id)
    # আগে থেকে দুজনের মধ্যে চ্যাট আছে কি না চেক
    convo = Conversation.objects.annotate(n=Count('participants')).filter(n=2, participants=request.user).filter(participants=target_user).first()

    if not convo:
        convo = Conversation.objects.create()
        convo.participants.add(request.user, target_user)
    
    return redirect('chat_detail', convo_id=convo.id)