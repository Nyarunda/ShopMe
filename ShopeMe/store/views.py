from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *

from .utils import cookiesCart

# Create your views here.


def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookiesData = cookiesCart(request)
        cartItems = cookiesData['cartItems']
        order = cookiesData['order']
        items = cookiesData['items']

    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookiesData = cookiesCart(request)
        cartItems = cookiesData['cartItems']
        order = cookiesData['order']
        items = cookiesData['items']

    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cookiesData = cookiesCart(request)
        cartItems = cookiesData['cartItems']
        order = cookiesData['order']
        items = cookiesData['items']

    context = {'items': items, 'order': order,
               'cartItems': cartItems, 'shipping': False}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('pro', productId)
    print('acti', action)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was Added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    print(data)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        print(total)

        if total == order.get_cart_total:
            order.complete = True
            print('cart Total', total)
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                zipcode=data['shipping']['zipcode'],
            )
    else:
        print('User Not Authenticated')
    return JsonResponse('Payment Completed', safe=False)


def main(request):
    context = {}
    return render(request, 'store/main.html', context)


def accounts(request):

    context = {}
    return render(request, 'store/my-account.html', context)
