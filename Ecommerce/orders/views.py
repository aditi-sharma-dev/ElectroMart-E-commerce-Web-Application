from django.shortcuts import render,redirect
from .models import *
from cart.models import Cart,CartItem

def checkout(request):
    if request.method=="POST":
        name=request.POST['name']
        phone=request.POST['phone']
        address=request.POST['address']
        city=request.POST['city']
        state=request.POST['state']
        pincode=request.POST['pincode']
        cart=Cart.objects.get(user=request.user)
        cart_items=CartItem.objects.filter(cart=cart)
        total_price=0
        for item in cart_items:
            total_price += item.product.price * item.quantity
        order=Order.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            total_price=total_price
        )
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
                )
        cart_items.delete()
        return redirect('order_success')
    
        
        
    return render(request,'checkout.html')
def my_orders(request):
    orders=Order.objects.filter(user=request.user).order_by('created_at')
    return render(request,'my_orders.html',{'orders':orders})
def order_success(request):
    return render(request,'order_success.html')


