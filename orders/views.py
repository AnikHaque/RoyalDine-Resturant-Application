from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from menu.models import Food


@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('menu')

    # প্রাইস এবং কোয়ান্টিটি ক্যালকুলেশন (float/int নিশ্চিত করা হয়েছে)
    total = sum(float(item['price']) * int(item['qty']) for item in cart.values())

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_price=total
        )

        for item_id, item in cart.items():
            if str(item_id).startswith('combo_'):
                # ১. কম্বো ডিল সেভ করার জন্য
                OrderItem.objects.create(
                    order=order,
                    food=None,  # ডাটাবেজে এখন এটি null হতে পারবে
                    combo_id=int(item['product_id']), # সরাসরি আইডি ব্যবহার
                    price=item['price'],
                    quantity=item['qty']
                )
            else:
                # ২. নরমাল খাবার সেভ করার জন্য
                try:
                    OrderItem.objects.create(
                        order=order,
                        food_id=int(item_id), # সরাসরি ফুড আইডি ব্যবহার
                        combo=None,
                        price=item['price'],
                        quantity=item['qty']
                    )
                except (Food.DoesNotExist, ValueError):
                    continue

        # কার্ট খালি করা
        request.session['cart'] = {}
        messages.success(request, "অর্ডারটি সফলভাবে সম্পন্ন হয়েছে!")
        return redirect('payment_page', order_id=order.id)

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'total': total
    })

@login_required
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    # Stripe checkout এ redirect
    return redirect('create_payment', order_id=order.id)


@login_required
def payment_success(request):
    return render(request, 'orders/success.html')

@login_required
def my_orders(request):
    # Logged-in user er sob orders
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'orders/my_orders.html', {
        'orders': orders
    })


@login_required
def mark_paid(request, order_id):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized.")
        return redirect('dashboard')

    order = get_object_or_404(Order, id=order_id)
    order.status = 'PAID'
    order.save()

    messages.success(request, f"Order #{order.id} marked as PAID.")
    return redirect('staff_dashboard')


def delete_order(request, order_id):
    # এখানে get_object_or_404 ব্যবহার করলে শুধু ওই আইডিটাই ধরা পড়বে
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if request.method == 'POST':
        order.delete() # শুধুমাত্র এই অর্ডারটি ডিলিট হবে
        messages.success(request, f"Order #{order_id} has been deleted.")
    
    return redirect('customer_dashboard')