
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('vendor-register/', views.registerVendor, name='vendor-register'),
]