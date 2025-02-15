from django.shortcuts import render
from django.http import HttpResponse
from .models import Product

# Create your views here.
def home(request):
    products = Product.objects.all()
    return render(request,"store/home.html",{'products':products})

def about(request):
    return render(request,"about.html")