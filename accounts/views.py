from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import CustomerRegisterForm, LoginForm
from .decorators import customer_required, staff_required, manager_required

from orders.models import Order

def register_view(request):
    if request.user.is_authenticated:
        return redirect('menu')

    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)

            # 🔒 ensure public register = customer
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
            return redirect('menu')
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




@login_required
def dashboard(request):
    # Redirect staff users to staff dashboard
    if request.user.is_staff:
        return redirect('staff_dashboard')

    # Normal user: show their orders
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/dashboard/dashboard.html', {
        'orders': orders
    })


@login_required
def staff_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, "You are not authorized to access this page.")
        return redirect('dashboard')

    # Staff can see all orders
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'accounts/dashboard/staff_dashboard.html', {
        'orders': orders
    })