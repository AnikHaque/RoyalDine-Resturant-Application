from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomerRegisterForm, LoginForm
from django.contrib.auth.decorators import login_required
from .decorators import staff_required, manager_required

def register_view(request):
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('menu')
    else:
        form = CustomerRegisterForm()

    return render(request, 'auth/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('menu')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


# 👤 Normal logged-in user (customer)
@login_required
def user_dashboard(request):
    return render(request, 'accounts/user_dashboard.html')


# 🍳 Staff only page
@staff_required
def staff_dashboard(request):
    return render(request, 'accounts/staff_dashboard.html')


# 🧑‍💼 Manager only page
@manager_required
def manager_dashboard(request):
    return render(request, 'accounts/manager_dashboard.html')