import stripe
from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from orders.models import Order

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_checkout_session(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],

        line_items=[{
            'price_data': {
                'currency': 'usd',   # change if needed
                'product_data': {
                    'name': f'Order #{order.id}',
                },
                'unit_amount': int(order.total_price * 100),
            },
            'quantity': 1,
        }],

        mode='payment',

        success_url='http://127.0.0.1:8000/orders/success/',
        cancel_url='http://127.0.0.1:8000/orders/cancel/',
    )

    # 🔥 THIS IS THE MAGIC LINE
    return redirect(session.url)
