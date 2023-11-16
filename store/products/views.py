from django.shortcuts import render

# Create your views here.

def index(request):
    context = {
        "title": "Главная страница UPGrade PC"
    }
    return render(request, 'products/index.html', context)

def products(request):
    context = {
        "title": "UPGrade PC - Каталог"
    }
    return render(request, 'products/products.html', context)
