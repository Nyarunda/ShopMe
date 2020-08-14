import json
from .models import *


def cookiesCart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart = {}
    print('cart', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
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
                },
                'quantity': cart[i]['quantity'],
                'get_total': total
            }
            items.append(item)
            if product.digital == False:
                order['shipping'] = True
        except:
            pass
    return {'order': order,  'cartItems': cartItems, 'items': items}

def cartData(request):
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
    return {'order': order,  'cartItems': cartItems, 'items': items}

def guestOrder(request, data):
    print('User Not Authenticated')
    print('COOKIES:', request.COOKIES)

    name = data['form']['fname']
    email = data['form']['email']
    cookiesData = cookiesCart(request)
    items = cookiesData['items']
    customer, created = Customer.objects.get_or_create(
        email=email,
    )
    customer.fname = name
    customer.save()

    order = Order.objects.create(
        customer=customer,
        complete=False
    )
    for item in items:
        product = Product.objects.get(
            id=item['product']['id']
        )
        orderItem = OrderItem.objects.create(
            product=product,
            order=order,
            quantity=item['quantity']
        )
    return customer, order