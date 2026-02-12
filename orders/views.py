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

    total = sum(item['price'] * item['qty'] for item in cart.values())

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_price=total
        )

        for item_id, item in cart.items():
            try:
                food = Food.objects.get(id=item_id)
            except Food.DoesNotExist:
                continue  # skip if food was deleted

            OrderItem.objects.create(
                order=order,
                food=food,          # ✅ use ForeignKey
                price=item['price'],
                quantity=item['qty']
            )

        # Clear cart
        request.session['cart'] = {}
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
