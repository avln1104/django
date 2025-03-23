from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import RegisterForm, LoginForm, PasswordResetRequestForm
from django.core.mail import send_mail
from django.conf import settings
import random

def home(request):
    return render(request, 'accounts/home.html', {'user': request.user})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # 'home' nomli sahifangiz bo‘lsa
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            code = ''.join([str(random.randint(0, 9)) for _ in range(6)])  # 6 raqamli kod
            request.session['reset_code'] = code
            request.session['reset_email'] = email

            # Email yuborish
            send_mail(
                'Parolni tiklash kodi',
                f'Sizning parolni tiklash kodingiz: {code}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            return redirect('password_reset_confirm')  # Keyingi qadam uchun
    else:
        form = PasswordResetRequestForm()
    return render(request, 'accounts/password_reset.html', {'form': form})

# Bu funksiya kodingizni tasdiqlash uchun qo‘shimcha sahifa bo‘ladi
def password_reset_confirm(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        if code == request.session.get('reset_code'):
            return redirect('home')  # Bu yerda yangi parol kiritish logikasini qo‘shishingiz mumkin
        else:
            return render(request, 'accounts/password_reset_confirm.html', {'error': 'Noto‘g‘ri kod'})
    return render(request, 'accounts/password_reset_confirm.html')