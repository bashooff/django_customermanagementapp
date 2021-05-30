from django.shortcuts import render

# Create your views here.

def home(requests):
    return render(requests, 'accounts/dashboard.html')

def products(requests):
    return render(requests, 'accounts/products.html')

def customer(requests):
    return render(requests, 'accounts/customer.html')