import qrcode
import base64
from io import BytesIO
from datetime import date as dt_date

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import JsonResponse

# আপনার অ্যাপের মডেল
from .models import Reservation, TableCapacity

@login_required
def book_table(request):
    if request.method == 'POST':
        date = request.POST.get('date')
        shift = request.POST.get('shift')
        guests = int(request.POST.get('guests'))
        
        if guests > 20:
            messages.error(request, "Sorry, we cannot accommodate more than 20 guests.")
            return render(request, 'tablebooking/reservation.html', {'today': dt_date.today()})

        with transaction.atomic():
            capacity, created = TableCapacity.objects.get_or_create(
                date=date, shift=shift, defaults={'total_tables': 15}
            )

            if capacity.available_tables > 0:
                res = Reservation.objects.create(
                    user=request.user, 
                    name=request.POST.get('name'),
                    email=request.POST.get('email'), 
                    phone=request.POST.get('phone'),
                    guest_count=guests, 
                    date=date, 
                    shift=shift
                )
                capacity.booked_tables += 1
                capacity.save()
                return redirect('reservation_success', booking_id=res.booking_id)
            else:
                messages.error(request, f"Full! No tables available for {date} during {shift} shift.")
    
    return render(request, 'tablebooking/reservation.html', {'today': dt_date.today()})

@login_required
def reservation_success(request, booking_id):
    reservation = get_object_or_404(Reservation, booking_id=booking_id)
    
    # QR Code জেনারেশন
    qr_content = f"ID: {reservation.booking_id}\nName: {reservation.name}\nDate: {reservation.date}\nShift: {reservation.shift}"
    qr = qrcode.QRCode(version=1, border=2, box_size=10)
    qr.add_data(qr_content)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    return render(request, 'tablebooking/success.html', {
        'reservation': reservation,
        'qr_code': qr_code_base64
    })

@login_required
def my_bookings(request):
    # ড্যাশবোর্ডের জন্য এই ফাংশনটি কাজ করবে
    bookings = Reservation.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'tablebooking/my_bookings.html', {'bookings': bookings})

def check_availability(request):
    date = request.GET.get('date')
    shift = request.GET.get('shift')
    capacity = TableCapacity.objects.filter(date=date, shift=shift).first()
    available = capacity.available_tables if capacity else 15
    return JsonResponse({'available': available})