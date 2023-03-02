from django.shortcuts import render
from django.http import HttpResponse, JsonResponse 
import json
import datetime
from .models import *
from django_daraja.mpesa.core import MpesaClient


# Create your views here.

def store(request):
    # if request.user.is_authenticated:
    #     customer = request.user.customer
    #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
    #     items = order.orderitem_set.all()
    #     cartItems = order.get_cart_items
    # else:
    #     items = []
    #     order = {'get_cart_total':0, 'get_cart_items':0 }
    #     cartItems = order['get_cart_items']

        products = Product.objects.all()
        context = {'products':products}
        return render(request, 'store/store.html', context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'delivery':False}

    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)    


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0, 'delivery':False}

    context = {'items':items, 'order':order}
    return render(request, 'store/checkout.html', context)  


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('productId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.delivery == True:
            DeliveryAddress.objects.create(
                customer=customer,
                order=order,
                address=data['delivery']['address'],
                city=data['delivery']['city'],
                county=data['delivery']['county'],
                street=data['delivery']['street'],
                location=data['delivery']['location'],
            )

    else:
        print('User is not logged in...')

    return JsonResponse('Payment Complete!', safe=False)

def mpesa(request):
    cl = MpesaClient()
    phone_number = '0740116783'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
    return HttpResponse(response)

def stk_push_callback(request):
    data = request.body

    return HttpResponse("Stk push")



