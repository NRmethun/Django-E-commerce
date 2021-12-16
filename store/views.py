from django.http import JsonResponse
from django.shortcuts import render

from .models import *
from .utils import cookiesCart ,cookieData ,guestOrder

import json
import datetime
# Create your views here.

def store(request):

    cookieData =cookiesCart(request) 
    cartItems = cookieData['cartItems']
    

    products =Product.objects.all() 
    context={'products':products , 'cartItems': cartItems } 
    return render(request,'store/store.html' , context ) 

def cart(request):

    cookieData =cookiesCart(request) 
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

        # cookieData =cookiesCart(request) 


    context={'items':items , 'order' :order ,'cartItems': cartItems} 
    return render(request,'store/Cart.html' , context ) 

from django.views.decorators.csrf import csrf_protect

@csrf_protect   
def checkout(request):
    
    cookieData =cookiesCart(request) 
    cartItems = cookieData['cartItems']
    order = cookieData['order']
    items = cookieData['items']

    context={'items':items , 'order' :order ,'cartItems': cartItems} 
    return render(request,'store/Checkout.html' , context ) 

def update_item(request): 
    data =json.loads(request.body)
    productId = data['productId'] 
    action =data['action'] 
    print('Action: ',action) 
    print('product: ', productId) 

    customer = request.user.customer 
    product =Product.objects.get(id=productId)
    order , created   = Order.objects.get_or_create(customer=customer,complete=False) 
    orderItem , created =OrderItem.objects.get_or_create(order=order ,product=product)
   
    if action == "add" :
       print('add hit ! ')
       orderItem.quantity = (orderItem.quantity+1) 

    elif action =="remove" :
        print('remove hit ! ')
        orderItem.quantity = (orderItem.quantity-1) 
    
    orderItem.save() 

    if orderItem.quantity <=0 :
        orderItem.delete() 


    return JsonResponse('hello from views ... ',safe=False ) 


def processOrder(request):
    data =json.loads(request.body) 
    transaction_id = datetime.datetime.now().timestamp()
    # print('data : ',request.body) 

    if request.user.is_authenticated :
        customer = request.user.customer 
        order , created   = Order.objects.get_or_create(customer=customer,complete=False) 
        
    
    else :
        customer , order = guestOrder(request,data)

    total =float(data['form']['total'] )
    order.transaction_id =transaction_id 
        
    if total == order.get_cart_total :
        order.complete =True 
    order.save() 

    if order.shipping == True :
        ShippingAddress.objects.create(
                customer =customer ,
                order =order ,
                address =data['shipping']['address'] , 
                city =data['shipping' ]['city'] ,
                state =data['shipping']['state'] ,
                zipcode =data['shipping']['zipcode'] ,
            )
        print('nothing')

    return JsonResponse('payment complete',safe=False ) 
