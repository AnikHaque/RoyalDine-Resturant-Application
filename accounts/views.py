from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomerRegisterForm, LoginForm
from .decorators import customer_required, staff_required, manager_required
from orders.models import Order
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
import json

# -------------------------------
# Authentication Views
# -------------------------------

def register_view(request):
    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # 🔒 Ensure public register = customer
            user.is_staff = False
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('menu')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = CustomerRegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Logged in successfully')

            # Redirect based on role
            if request.user.is_staff:
                return redirect('staff_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Logged out successfully')
    return redirect('home')


# -------------------------------
# Customer Dashboard
# -------------------------------

@login_required
def dashboard(request):
    if request.user.is_staff:
        return redirect('staff_dashboard')
    # normal customer
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/dashboard/customer_dashboard.html', {'orders': orders})

@login_required
def customer_dashboard(request):
    # Normal user orders
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/dashboard/customer_dashboard.html', {
        'orders': orders
    })

@login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('dashboard')

    status_filter = request.GET.get('status')
    if status_filter in ['PAID', 'PENDING']:
        orders = Order.objects.filter(status=status_filter).order_by('-created_at')
    else:
        orders = Order.objects.all().order_by('-created_at')

    return render(request, 'accounts/dashboard/staff_dashboard.html', {
        'orders': orders
    })
@login_required
def staff_analytics(request):
    if not request.user.is_staff:
        return redirect('dashboard')

    # Orders per day
    orders_per_day = (
        Order.objects
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    dates = [str(x['date']) for x in orders_per_day]
    counts = [x['count'] for x in orders_per_day]

    # Revenue per day
    revenue = (
        Order.objects
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(total=Sum('total_price'))
        .order_by('date')
    )

    revenue_totals = [float(x['total'] or 0) for x in revenue]

    # Status distribution
    status_data = (
        Order.objects
        .values('status')
        .annotate(count=Count('id'))
    )

    status_labels = [x['status'] for x in status_data]
    status_counts = [x['count'] for x in status_data]

    context = {
        'dates': json.dumps(dates),
        'counts': json.dumps(counts),
        'revenue': json.dumps(revenue_totals),
        'status_labels': json.dumps(status_labels),
        'status_counts': json.dumps(status_counts),
    }

    return render(request, 'accounts/dashboard/staff_analytics.html', context)

@login_required
def manager_dashboard(request):
    if not request.user.is_superuser:
        messages.error(request, "You are not authorized.")
        return redirect('dashboard')
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'accounts/dashboard/manager_dashboard.html', {'orders': orders})


# -------------------------------
# Staff Action: Mark Order Paid
# -------------------------------

@login_required
@staff_required
def mark_paid(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.status = 'PAID'
    order.save()
    messages.success(request, f'Order #{order.id} marked as Paid')
    return redirect('staff_dashboard')
