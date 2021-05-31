from django.shortcuts import render
from .models import *

# Create your views here.

def home(requests):
    orders = Order.objects.all()
    customers = Customer.objects.all()

    total_customer = customers.count()

    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders':orders, 'customers':customers,
                'total_orders':total_orders, 'delivered':delivered,
                'pending':pending}
    
    return render(requests, 'accounts/dashboard.html', context)

def products(requests):
    products = Product.objects.all()
    context = {'products':products}
    return render(requests, 'accounts/products.html', context)

def customer(requests, pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    context = {'customer':customer, 'orders':orders, 'order_count':order_count}
    return render(requests, 'accounts/customer.html', context)

def createOrder(request):
    
    context = {}
    return render(request, 'accounts/order_form.html', context)