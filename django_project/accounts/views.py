from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter

def registerPage(requests):
    form = CreateUserForm()

    if requests.method == 'POST':
        form = CreateUserForm(requests.POST)
        if form.is_valid():
            form.save()
            user=form.cleaned_data.get('username')
            messages.success(requests, 'Account was created for ' + user)

            return redirect('login')

    context = {'form':form}
    return render(requests, 'accounts/register.html', context)

def loginPage(requests):

    if requests.method == 'POST':
        username = requests.POST.get('username')
        password = requests.POST.get('password')

        user = authenticate(requests, username=username, password=password)

        if user is not None:
            login(requests, user)
            return redirect('home')
        else:
            messages.info(requests, 'Username or password is incorrect')
            

    context = {}
    return render(requests, 'accounts/login.html', context)

def logoutUser(requests):
    logout(requests)
    return redirect('Login')

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

    myFilter = OrderFilter(requests.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer':customer, 'orders':orders, 'order_count':order_count,
                'myFilter':myFilter}
    return render(requests, 'accounts/customer.html', context)

def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'))
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
    #form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
            
    context = {'formset':formset}
    return render(request, 'accounts/order_form.html', context)

def updateOrder(request, pk):

	order = Order.objects.get(id=pk)
	form = OrderForm(instance=order)

	if request.method == 'POST':
		form = OrderForm(request.POST, instance=order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {'form':form}
	return render(request, 'accounts/order_form.html', context)

def deleteOrder(request, pk):
	order = Order.objects.get(id=pk)
	if request.method == "POST":
		order.delete()
		return redirect('/')

	context = {'item':order}
	return render(request, 'accounts/delete.html', context)