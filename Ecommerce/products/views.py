from django.shortcuts import render, redirect,get_object_or_404
from cart.models import Cart, CartItem
from django.contrib.auth.decorators import login_required
from.models import *

def home(request):
    categories = Category.objects.all()

    products = []

    for category in categories:
        product = Product.objects.filter(category=category).first()
        if product:
            products.append(product)

    products = products[:4]

    context = {
        'categories': categories,
        'products': products
    }

    return render(request, 'products/home.html', context)
    
    
def product_list(request):
    products=Product.objects.all()
    categories=Category.objects.all()
    search=request.GET.get('q')
    if search:
        products=products.filter(name__icontains=search)
    category_id=request.GET.get('category')
    if category_id:
        products=products.filter(category_id=category_id)
    context={
            'products':products,
            'categories':categories
        }
        
    return render(request,'products/products.html',context)
def product_detail(request,id):
    #product=Product.objects.get(id=id)
    product=get_object_or_404(Product,id=id)
    return render(request,'products/product_detail.html',{'product':product})
    
@login_required
def order_now(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    if product.stock<=0:
        return redirect('product_detail',id=product_id)
    cart,created=Cart.objects.get_or_create(user=request.user)
    cart_item,created=CartItem.objects.get_or_create(cart=cart,product=product)
    if not created:
    
        if cart_item.quantity<product.stock:
            cart_item.quantity+=1
          
            cart_item.save()
        
    return redirect('checkout')