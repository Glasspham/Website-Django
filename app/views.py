from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.
def detail(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.getNumberOfProducts
    else: 
        items = []
        order = {'getNumberOfProducts' : 0, 'getTotalAmount' : 0}
        cartItems = order['getNumberOfProducts']
    id = request.GET.get('id', '')
    products = Product.objects.filter(id=id)
    categories  = Category.objects.filter(isSub=False)
    context = {'products':products, 'items':items, 'order':order, 'cartItems':cartItems, 'categories':categories}
    return render(request, 'app/detail.html', context)

def category(request):
    categories  = Category.objects.filter(isSub=False)
    active_category = request.GET.get('category', '')
    if active_category:
        products = Product.objects.filter(category__slug=active_category)
    context = {'categories':categories, 'products':products, 'active_category':active_category}
    return render(request, 'app/category.html', context)

def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__icontains=searched)
    else:
        keys = []
        searched = ""
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.getNumberOfProducts
    else: 
        order = {'getNumberOfProducts' : 0, 'getTotalAmount' : 0}
        cartItems = order['getNumberOfProducts']
    categories  = Category.objects.filter(isSub=False)
    products = Product.objects.all()
    context = {'products' : products, 'cartItems':cartItems, 'searched':searched, 'keys':keys, 'categories':categories}
    return render(request, 'app/search.html', context)

def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    categories  = Category.objects.filter(isSub=False)
    context = {'form':form, 'cartItems':0, 'categories':categories}
    return render(request, 'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request,"User or password not correct!")
    categories  = Category.objects.filter(isSub=False)
    context = {'cartItems':0, 'categories':categories}
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.getNumberOfProducts
    else: 
        items = []
        order = {'getNumberOfProducts' : 0, 'getTotalAmount' : 0}
        cartItems = order['getNumberOfProducts']
    products = Product.objects.all()
    categories  = Category.objects.filter(isSub=False)
    context = {'products' : products, 'cartItems':cartItems, 'categories':categories}
    return render(request, 'app/home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.getNumberOfProducts
    else: 
        items = []
        order = {'getNumberOfProducts' : 0, 'getTotalAmount' : 0}
        cartItems = order['getNumberOfProducts']
    categories  = Category.objects.filter(isSub=False)
    context = {'items' : items, 'order' : order, 'cartItems':cartItems, 'categories':categories}
    return render(request, 'app/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.getNumberOfProducts
    else: 
        items = []
        order = {'getNumberOfProducts' : 0, 'getTotalAmount' : 0}
        cartItems = order['getNumberOfProducts']
    categories  = Category.objects.filter(isSub=False)
    context = {'items' : items, 'order' : order, 'cartItems':cartItems, 'categories':categories}
    return render(request, 'app/checkout.html', context)

def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added', safe=False)
