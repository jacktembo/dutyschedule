from django.contrib.auth import login, load_backend, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, \
    PasswordChangeForm
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import NewUserForm
from django.contrib.auth.models import User
from dutyrota.utils import OneTimePassword
import random
from django.core.mail import send_mail


def generate_otp():
    """generating one time password"""
    start = 100000
    stop = 900000
    return random.randrange(start, stop)


def dashboard(request):
    """Dashboard where a user is redirected after they login"""
    return HttpResponse('welcome to the dashboard')


def register(request):
    """"Registering users in the system"""
    if request.method != 'POST':
        form = NewUserForm()
    else:
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse('routine:dashboard'))
        else:
            form = NewUserForm()
            return render(request, "accounts/register.html", {"form": form})

    return render(request, "accounts/register.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    """Login a user in"""
    if request.method != "POST":
        form = AuthenticationForm()
        return render(request, "accounts/login.html", {"form": form})
    else:
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)

        user = authenticate(request, username=username, password=password)
        if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('routine:today-rota'))
        else:
            return HttpResponse("something went wrong.")


def change_password(request):
    """Changing user password"""
    if request.method != "POST":
        user = request.user
        form = PasswordChangeForm(user)
        return render(request, "accounts/password_change.html", {"form": form})
    else:
        user = request.user
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            """Keep a user logged in after Changing their password"""
            update_session_auth_hash(request, form.user)
            return redirect('/accounts/dashboard')


def password_reset_confirm(request, email):
    """entering one time password sent """
    if request.method != 'POST':
        return render(request, 'accounts/password_reset_confirm.html')
    else:
        otp = request.POST.get('otp', False)
        # otps sent to this email.
        db_otps = OneTimePassword.objects.filter(email=email).all()
        # getting otp values of the user
        result = [value.otp for value in db_otps]
        if otp in result:
            user = User.objects.get(email=email)
            login(request, user)  # Log the user in and redirect them.
            return HttpResponse('success')
        else:
            return HttpResponse('incorrect otp')


def password_reset(request):
    if request.method != 'POST':
        return render(request, 'accounts/password_reset.html')
    else:
        try:
            email_address = request.POST.get('email', False)
            user = User.objects.get(email=email_address)
            otp_number = generate_otp()  # generated otp.
            # Create otp object.
            otp = OneTimePassword(
                user=user, otp=otp_number, email=email_address)
            otp.save()  # Save one time password to database.
            subject = 'Your One Time Password'
            message = f"Your one time password is {otp_number}"
            email_from = 'no-reply@jacktembo.com'
            recipient_list = [str(user.email)]
            send_mail(subject, message, email_from, recipient_list)
            return HttpResponseRedirect(reverse('password-reset-confirm', args=(email_address,)))

        except NameError:
            return HttpResponse('email not resgistered')
