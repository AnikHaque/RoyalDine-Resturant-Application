from django.contrib import admin
from django.urls import path, include
from core import views as core_views # core অ্যাপ থেকে ভিউ আনুন

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', core_views.home, name='home'), # এখন হোমপেজ আসবে core অ্যাপ থেকে
    path('booking/', include('tablebooking.urls')),
]