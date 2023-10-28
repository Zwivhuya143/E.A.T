from django.http import HttpResponse
from django.template import loader
from shop.models import Product, Cart, CartItem, Category, Order, OrderItem
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from shop.forms import LoginForm, RegisterForm, CheckoutForm

import json


def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})    
   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid(): #if form is valid
            user = form.save(commit=False) #create user from form but don't commit to database
            user.username = user.username.lower() #update username to lowercase
            user.save() #commit user to database

            #get user from database
            user_obj=User.objects.filter(username=user.username).first()
            #create a cart for newly registered user
            Cart(cart_status="active", user=user_obj).save()
            messages.success(request, 'You have signed up successfully.')
            login(request, user)
            return redirect('index') #redirect user to homepage
        else:
            messages.error(request, "Something went wrong, please check your input")
            return render(request, 'register.html', {'form': form})

def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'login.html', {'form': form})    
   
    if request.method == 'POST':
        form = LoginForm(request.POST) 
        if form.is_valid(): #if form is valid
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password) #authenticate user
            if user is not None:
                login(request, user) #login user
                return redirect('index') #redirect user to homepage
            else:
                messages.error(request, "Invalid username or password")
                return render(request, 'login.html', {'form': form})
        else:
            messages.error(request, "Something went wrong, please check your input")
            return render(request, 'login.html', {'form': form})
        
def sign_out(request):
    logout(request)
    return redirect('index')


@login_required
def get_my_orders(request):
    user = request.user
    orders = Order.objects.filter(user__id=user.id).all()
    template = loader.get_template("orders.html")
    context = {
        "orders": orders,
    }
    return HttpResponse(template.render(context, request))

def order_details(request, order_id):
    user = request.user
    order = Order.objects.filter(user__id=user.id, order_id=order_id).first()
    order_items = OrderItem.objects.filter(order=order).all()
    template = loader.get_template("order_details.html")
    context = {
        "order": order,
        "order_items": order_items,
    }
    return HttpResponse(template.render(context, request))


def get_reservations(request):
    template = loader.get_template("reservations.html")
    return HttpResponse(template.render({},request))


def add_to_cart(request, product_id):
    user = request.user
    user_cart = Cart.objects.get(user_id=user.id) #getting the current users cart
    
    product = Product.objects.get(product_id=product_id) #getting product object
    cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=product) #gets or create cart item
    # If cart item exists, just increase its quantity
    cart_item.quantity = cart_item.quantity + 1
    cart_item.save()
    messages.success(request, "Cart updated!")

    return redirect('cart')


def remove_from_cart(request, product_id):
    user = request.user

    user_cart = Cart.objects.get(user__id=user.id) #getting the current users cart
    cart_item = CartItem.objects.get(cart=user_cart, product__product_id=product_id) #getting cart item
    cart_item.delete() #deleting cart item

    return redirect('cart')
    

def update_item_quantity(request, product_id):
    user = request.user
    if request.method == "POST":
        user_cart = Cart.objects.get(user__id=user.id) #getting the current users cart
        product = Product.objects.get(product_uuid=product_id) #getting product object
        cart_item = CartItem.objects.get(cart=user_cart, product=product) #getting cart item
        cart_item.quantity = request.POST.get('quantity') # updating cart item quantity
        cart_item.save()

        return redirect('cart')
    

def checkout(request):
    if request.method == 'GET':
        form = CheckoutForm()
        return render(request, 'checkout.html', {'form': form}) 
    if request.method == 'POST':
        form = CheckoutForm(request.POST) 
        if form.is_valid():
            user = request.user
            user_cart = Cart.objects.get(user__id=user.id)
            cart_items = CartItem.objects.filter(cart=user_cart).all()
            cart_total = 0
            for item in cart_items:
                cart_total += item.product.price * item.quantity
            #create order
            order = Order(user=user, address=form.cleaned_data['address'], order_status="accepted", total_price=cart_total)
            order.save()
            #create order items
            for item in cart_items:
                order_item = OrderItem(order=order, product=item.product, quantity=item.quantity)
                order_item.save()
            #delete cart items
            cart_items.delete()

            return redirect('index')
    return render(request, 'checkout.html', {'form': form})


def get_menu(request):
    products = Product.objects.all()
    template = loader.get_template("menu.html")
    context = {
        "menuProducts": products,
    }
    return HttpResponse(template.render(context,request))

def get_blog(request):
    template = loader.get_template("blog.html")
    return HttpResponse(template.render({},request))


# user = request.user
#     cart = []
#     cart = Cart.objects.filter(user__id=user.id).first()
#     template = loader.get_template("checkout.html")    
#     cart_items = CartItem.objects.filter(cart=cart).all()
#     context = {
#         "cart_items": cart_items,
#     }
#     return HttpResponse(template.render(context, request))
def emptyIndex(request):
    template = loader.get_template("index.html")
    context = {}
    return HttpResponse(template.render(context, request))

def index(request, slug=None):
    if slug is None:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(category__slug=slug).all()

    categories = Category.objects.all()

    template = loader.get_template("index.html")
    context = {
        "products": products,
        "categories": categories,
    }
    return HttpResponse(template.render(context,request))


        
def cart(request):
    user = request.user
    user_cart = Cart.objects.get(user__id=user.id)
    cart_items = CartItem.objects.filter(cart=user_cart).all()
    cart_total = 0
    for item in cart_items:
        cart_total += item.product.price * item.quantity
    template = loader.get_template("cart.html")
    context = {
        "cart_items": cart_items,
        "cart_total": cart_total,
    }
    return HttpResponse(template.render(context, request))

