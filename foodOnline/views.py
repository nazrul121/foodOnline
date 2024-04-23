from django.shortcuts import render
from foodOnline import views

def home(request):
    return render(request, 'frontend/home.html')