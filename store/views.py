from django.shortcuts import render, redirect
import json

from django.urls import reverse

from store.models import Product, Customer, Order, OrderItem
from django.http import JsonResponse, HttpResponseRedirect
from .forms import ProductForm
from django.contrib import messages


def store(request):
    if request.user.is_authenticated:
        # customer = request.user.customer
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer)
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        cartItems = 0
        for i in cart:
            cartItems += cart[i]['quantity']
    category = {
        'Cloths': ['T-Shirt', 'cap', 'trouser'],
        'Electronics': ['Computer', 'mobile', 'watch'],
        'Food': ['Nepali', 'Chinese', 'Danish'],
        #'Beverages': ['cold', 'hot']
    }
    electronics = ['Computer', 'mobile', 'watch'],
    products = Product.objects.all()

    return render(request, 'store/store.html', {'products': products, 'cartItems': cartItems, 'category': category, 'electronics':electronics})


def detail_view(request, id):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        cartItems = 0
        for i in cart:
            cartItems += cart[i]['quantity']
    product = Product.objects.get(id=id)
    return render(request, 'store/detail.html', {'product': product, 'cartItems': cartItems})


def update_item(request):
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    if action == 'delete':
        print('action delete')
        OrderItem.objects.filter(product=product).delete()
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
    else:
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        order_item, created = OrderItem.objects.get_or_create(
            product=product, order=order)
        if action == 'add':
            order_item.quantity = order_item.quantity + 1
        elif action == 'remove':
            order_item.quantity = order_item.quantity - 1
        order_item.save()
        if order_item.quantity <= 0:
            order_item.delete()
    return JsonResponse(order.get_cart_items, safe=False)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}

        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']

        for i in cart:
            try:
                cartItems += cart[i]['quantity']
                product = Product.objects.get(id=i)

                total = (product.price * cart[i]['quantity'])
                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']

                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                        'digital': product.digital
                    },
                    'quantity': cart[i]["quantity"],
                    'get_total': total
                }
                items.append(item)

            except:
                pass

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        total = order.get_cart_items
        total_cost = order.get_cart_total
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
        cartItems = order['get_cart_items']
        for i in cart:
            try:
                cartItems += cart[i]['quantity']
                product = Product.objects.get(id=i)
                total = (product.price * cart[i]['quantity'])
                order['get_cart_total'] += total
                order['get_cart_items'] += cart[i]['quantity']
                item = {
                    'product': {
                        'id': product.id,
                        'name': product.name,
                        'price': product.price,
                        'imageURL': product.imageURL,
                        'digital': product.digital
                    },
                    'quantity': cart[i]["quantity"],
                    'get_total': total
                }
                items.append(item)
            except:
                pass
        total = 0
        total_cost = 0
        total = sum(item['quantity'] for item in items)
        total_cost = sum(item['get_total'] for item in items)
    return render(request, 'store/checkout.html',
                  {'items': items, 'total': total, 'total_cost': total_cost, 'cartItems': cartItems})


def product_form(request):
    if request.method == 'POST':
        product = ProductForm(request.POST, request.FILES)
        if product.is_valid():
            product.save()
            name = product.cleaned_data.get('name')
            messages.success(request, f'{name} added into the product')
        return redirect('store')
    else:
        product = ProductForm()
    return render(request, 'store/product_form.html', {'product': product})


def payment(request):
    response = HttpResponseRedirect(reverse('store'))
    if not request.user.is_authenticated:
        customer, created = Customer.objects.get_or_create(user=None)
        order, created = Order.objects.get_or_create(customer=customer)
        response.delete_cookie('cart')
        print(request.COOKIES.get('cart'))
        # del request.COOKIES['cart']
        # import pdb; pdb.set_trace()
    else:
        customer, created = Customer.objects.get_or_create(user=request.user)
        order, created = Order.objects.get_or_create(customer=customer)
        order.delete()
        order.save()
    messages.success(request, f'purchase successfull')
    return response
