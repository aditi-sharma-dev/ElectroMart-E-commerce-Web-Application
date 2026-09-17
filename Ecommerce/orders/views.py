from django.shortcuts import render, redirect
from .models import *
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from accounts.models import Profile


@login_required
def checkout(request):

    cart = Cart.objects.filter(user=request.user).first()

    if not cart:
        return redirect('cart')



    if request.method == "POST" and 'selected_items' in request.POST:

        selected_items = request.POST.getlist('selected_items')

        if not selected_items:
            return redirect('cart')

        request.session['selected_items'] = selected_items

        return redirect('checkout')


  
    selected_items = request.session.get('selected_items')

    if not selected_items:
        return redirect('cart')

    cart_items = CartItem.objects.filter(
        cart=cart,
        id__in=selected_items
    )

    if not cart_items.exists():
        return redirect('cart')


    # TOTAL
    total_price = sum(
        item.product.price * item.quantity
        for item in cart_items
    )


    # PLACE ORDER
    if request.method == "POST":

        name = request.POST['name']
        phone = request.POST['phone']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']


        
        for item in cart_items:

            if item.quantity > item.product.stock:
                return redirect('cart')


        # CREATE ORDER
        order = Order.objects.create(

            user=request.user,
            name=name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
            total_price=total_price
        )


        # CREATE ORDER ITEMS
        for item in cart_items:

            OrderItem.objects.create(

                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

            item.product.stock -= item.quantity
            item.product.save()


        cart_items.delete()


        # SESSION CLEAR
        del request.session['selected_items']


        return redirect('order_success')


    # PROFILE
    profile, created = Profile.objects.get_or_create(
        user=request.user
    )


    return render(
        request,
        'checkout.html',
        {
            'profile': profile,
            'cart_items': cart_items,
            'total_price': total_price
        }
    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_orders.html',
        {
            'orders': orders
        }
    )


@login_required
def order_success(request):

    return render(
        request,
        'order_success.html'
    )