from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_view, name='cart'),
    
    # এখানে <int:food_id> এর বদলে <str:food_id> করে দিন
    path('add/<str:food_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<str:food_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update/<str:food_id>/<str:action>/', views.update_cart, name='update_cart'),
]