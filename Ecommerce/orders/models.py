from django.db import models
from products.models import Product
from django.contrib.auth.models import User
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=30)
    phone=models.CharField(max_length=10)
    address=models.TextField()
    city=models.CharField(max_length=30)
    state=models.CharField(max_length=30)
    pincode=models.CharField(max_length=10)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    status=models.CharField(max_length=20,default='Pending')
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Order{self.id}"
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    
    @property
    def item_total(self):
        return self.price * self.quantity
    def __str__(self):
        return self.product.name
    
