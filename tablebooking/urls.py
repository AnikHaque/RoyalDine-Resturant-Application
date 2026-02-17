from django.urls import path
from . import views

urlpatterns = [
    # বুকিং পেজ (টেমপ্লেটে book_table বা create_reservation যেটাই থাকুক কাজ করবে)
    path('book/', views.book_table, name='book_table'),
    path('create-reservation/', views.book_table, name='create_reservation'),
    
    # বুকিং লিস্ট/ইনভেন্টরি
    path('my-bookings/', views.my_bookings, name='reservation_list'),
    path('my-list/', views.my_bookings, name='my_bookings'),
    
    # বুকিং সাকসেস/কিউআর কোড
    path('success/<str:booking_id>/', views.reservation_success, name='reservation_success'),
    
    # এভেইল্যাবিলিটি চেক (AJAX এর জন্য)
    path('check-availability/', views.check_availability, name='check_availability'),
]