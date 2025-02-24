from django.urls import path
from payment import views

urlpatterns = [
   
    path("payment_success",views.payment_success, name='payment_success'),
    path("checkout",views.checkout, name='checkout'),
    
]

