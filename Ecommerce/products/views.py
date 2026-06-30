from django.shortcuts import render, get_object_or_404
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
    