from django.urls import path
from . import views   # ✅ এই লাইনটাই missing ছিল

urlpatterns = [
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('staff/', views.staff_dashboard, name='staff_dashboard'),
    path('manager/', views.manager_dashboard, name='manager_dashboard'),
]
