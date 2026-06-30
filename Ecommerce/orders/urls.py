from django.urls import path
from.import views

urlpatterns = [
    path('checkout/',views.checkout,name='checkout'),
    path('my_orders/',views.my_orders,name='my_orders'),
    path('order-success/',views.order_success,name='order_success'),
    
]