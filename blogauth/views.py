import random
import string

from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from blogauth.forms import RegisterForm, LoginForm
from blogauth.models import ValidationModel
from django.contrib.auth import get_user_model, login, logout

User = get_user_model()

# Create your views here.


@require_http_methods(["GET", "POST"])
def bloglogin(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            remember = form.cleaned_data.get("remember")
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                login(request, user)
                if not remember:
                    request.session.set_expiry(0)
                return redirect('/')
            else:
                print('password is incorrect')
                return redirect(reverse('blogauth:login'))
        else:
            print('email or password is incorrect')
            # form.add_error('email',"email or password is incorrect")
            # return render(request,"login.html",{'form':form})
            return redirect(reverse('blogauth:login'))


def bloglogout(request):
    logout(request)
    return redirect('/')


@require_http_methods(["GET", "POST"])
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('blogauth:login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def send_validation(request):
    email = request.GET.get('email')
    if not email:
        return JsonResponse({"code": 400, "message": "Email can not be empty!"})
    validation = "".join(random.sample(string.digits, 4))
    ValidationModel.objects.update_or_create(
        email=email, defaults={"validation": validation})
    send_mail("validation", message=f"Your validation is {
              validation}", recipient_list=[email], from_email=None)
    return JsonResponse({"code": 200, "message": "Email sending success"})
