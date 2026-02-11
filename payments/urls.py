from django.urls import path
from . import views

urlpatterns = [
    path('create/<int:order_id>/', views.create_payment_intent, name='create_payment'),
]
