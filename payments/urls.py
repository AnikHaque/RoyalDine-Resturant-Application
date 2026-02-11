from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:order_id>/', views.create_checkout_session, name='create_payment'),
]
