from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
def detail(request):
    user_not_login = "hidden"
    user_login = "show"
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items()  # Call the method to get cart items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    id = request.GET.get('id','')
    products = Product.objects.filter(id=id)
    categories = Category.objects.filter(is_sub =False)
    context = {'products':products,'categories': categories,'products': products, 'cartItems': cartItems, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/detail.html', context)
def category(request):
    categoreies = Category.objects.filter(is_sub =False)
    active_category = request.GET.get('category','')
    if active_category:
        products = Product.objects.filter(category__slug = active_category)
    context = {'categories':categoreies,'products':products,'active_category':active_category}
    return render(request,'app/category.html',context)
def about(request):
    user_not_login = "hidden"
    user_login = "show"

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []  # Khởi tạo giá trị mặc định là một danh sách trống
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        user_not_login = "hidden"
        user_login = "show"
    categories = Category.objects.filter(is_sub =False)
    context = {'categories': categories,'items': items, 'order': order, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/about.html')

def search(request):
    searched = ""
    keys = None
    cartItems = []  # Initialize cartItems to an empty list

    if request.method == "POST":
        searched = request.POST.get("searched")
        keys = Product.objects.filter(name__contains=searched)

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.get_cart_items()  # Call the method to get cart items
    
    products = Product.objects.all()
    return render(request, 'app/search.html', {'products':products,"searched": searched, "keys": keys, 'products': products, 'cartItems': cartItems})
    
def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context ={'form': form}
    return render(request, 'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'User or password not correct, try again!')
            
    context = {}
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    user_not_login = "hidden"
    user_login = "show"
    cartItems = 0  # Initialize cartItems to a default value

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items()  # Call the method to get cart items
        user_not_login = "hidden"
        user_login = "show"
    else:
        items = []
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        cartItems = order['get_cart_items']
        user_not_login = "show"
        user_login = "hidden"
    products = Product.objects.all()
    categories = Category.objects.filter(is_sub =False)
    context = {'categories': categories,'products': products, 'cartItems': cartItems, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/home.html', context)

def cart(request):
    user_not_login = "hidden"
    user_login = "show"

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []  # Khởi tạo giá trị mặc định là một danh sách trống
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        user_not_login = "hidden"
        user_login = "show"
    categories = Category.objects.filter(is_sub =False)
    context = {'categories': categories,'items': items, 'order': order, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/cart.html', context)

def checkout(request):
    user_not_login = "show"
    user_login = "hidden"

    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        user_not_login = "show"
        user_login = "hidden"
    else:
        items = []  # Khởi tạo giá trị mặc định là một danh sách trống
        order = {'get_cart_items': 0, 'get_cart_total': 0}
        user_not_login = "hidden"
        user_login = "show"

    context = {'items': items, 'order': order, 'user_not_login': user_not_login, 'user_login': user_login}
    return render(request, 'app/checkout.html', context)

def updateItem(request):
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
def clear_cart(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            customer = request.user
            order, created = Order.objects.get_or_create(customer=customer, complete=False)
            order.delete()  # Xóa toàn bộ đơn hàng
            return JsonResponse({'message': 'Cart cleared successfully'})
        else:
            return JsonResponse({'message': 'User not authenticated'}, status=401)