from django.shortcuts import render


# Create your views here.

def login(request):
    context = {
        "title": "Авторизация пользователя UPGrade PC"
    }
    return render(request, 'users/login.html', context)


def registration(request):
    context = {
        "title": "Регистрация нового пользователя UPGrade PC"
    }
    return render(request, 'users/registration.html', context)
