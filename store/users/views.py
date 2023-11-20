from django.shortcuts import render

from users.forms import UserLoginForm


# Create your views here.

def login(request):
    context = {
        "title": "Авторизация пользователя UPGrade PC",
        'login_form': UserLoginForm(),

    }
    return render(request, 'users/login.html', context)


def registration(request):
    context = {
        "title": "Регистрация нового пользователя UPGrade PC"
    }
    return render(request, 'users/registration.html', context)
