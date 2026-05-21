from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *


def home(request):

    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(
            name__icontains=query
        )
    else:
        products = Product.objects.all()

    categories = Category.objects.all()

    return render(
        request,
        'testapp/home.html',
        {
            'products': products,
            'categories': categories
        }
    )


def register_user(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('/login/')

    return render(request, 'testapp/register.html')


def login_user(request):

    if request.method == 'POST':

        username = request.POST['username']

        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/')

    return render(request, 'testapp/login.html')


def logout_user(request):

    logout(request)

    return redirect('/login/')


def add_to_cart(request, product_id):

    if not request.user.is_authenticated:
        return redirect('/login/')

    product = Product.objects.get(id=product_id)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('/cart/')


def cart_view(request):

    if not request.user.is_authenticated:
        return redirect('/login/')

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    items = CartItem.objects.filter(cart=cart)

    total = 0

    for item in items:
        total += item.product.price * item.quantity

    return render(
        request,
        'testapp/cart.html',
        {
            'items': items,
            'total': total
        }
    )


def remove_cart_item(request, item_id):

    item = CartItem.objects.get(id=item_id)

    item.delete()

    return redirect('/cart/')


def checkout(request):

    cart = Cart.objects.get(user=request.user)

    items = CartItem.objects.filter(cart=cart)

    total = 0

    for item in items:
        total += item.product.price * item.quantity

    order = Order.objects.create(
        user=request.user,
        total_price=total
    )

    for item in items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity
        )

    items.delete()

    return render(request, 'testapp/success.html')


@api_view(['GET'])
def product_api(request):

    products = Product.objects.all()

    serializer = ProductSerializer(
        products,
        many=True
    )

    return Response(serializer.data)