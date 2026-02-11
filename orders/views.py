from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem


@login_required
def checkout_view(request):
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, 'Your cart is empty')
        return redirect('menu')

    total = sum(item['price'] * item['qty'] for item in cart.values())

    if request.method == 'POST':
        order = Order.objects.create(
            user=request.user,
            total_price=total
        )

        for item in cart.values():
            OrderItem.objects.create(
                order=order,
                food_name=item['name'],
                price=item['price'],
                quantity=item['qty']
            )

        request.session['cart'] = {}

        messages.success(request, 'Order placed successfully')
        return redirect('user_dashboard')

    return render(request, 'orders/checkout.html', {
        'cart': cart,
        'total': total
    })
