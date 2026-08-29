from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from products.models import Product
from django.contrib.auth.decorators import login_required


@login_required
def cart_view(request):

    cart = Cart.objects.filter(user=request.user).first()

    cart_items = []
    grand_total = 0

    if cart:
        cart_items = CartItem.objects.filter(cart=cart)

        for item in cart_items:
            item.total_price = item.product.price * item.quantity
            grand_total += item.total_price

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total
    })


@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(Product, id=product_id)

    if product.stock <= 0:
        return redirect('product_detail', id=product_id)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        if cart_item.quantity < product.stock:
            cart_item.quantity += 1
            cart_item.save()

    return redirect('cart')


@login_required
def remove_cart_item(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    item.delete()

    return redirect('cart')


@login_required
def increase_quantity(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if item.quantity < item.product.stock:
        item.quantity += 1
        item.save()

    return redirect('cart')


@login_required
def decrease_quantity(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user
    )

    if item.quantity > 1:
        item.quantity -= 1
        item.save()

    return redirect('cart')