from django.urls import path
from .views import menu_view
from menu import views

urlpatterns = [
    path('', menu_view, name='menu'),
    path('category/<int:category_id>/', views.category_items, name='category_items'),
   
]
