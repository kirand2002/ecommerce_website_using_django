from django.db import models
from django.contrib.auth.models import User
from store.models import Product
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
import datetime


class ShippingAddress(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    shipping_full_name = models.CharField(max_length=250)
    shipping_email = models.CharField(max_length=250)
    shipping_address1 = models.CharField(max_length=250)
    shipping_address2 = models.CharField(max_length=250,  blank=True, null=True)
    shipping_city = models.CharField(max_length=250)
    shipping_state = models.CharField(max_length=250, blank=True, null=True)
    shipping_zipcode = models.CharField(max_length=250)
    shipping_country = models.CharField(max_length=250,blank=True, null=True)

    #dont pluralize address

    class Meta:
        verbose_name_plural = "shipping Address"


    def __str__(self):
        return f'Shipping Address - {str(self.id)}'
    

#create order model

class Order(models.Model):

    #foriegnkey
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    full_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    shipping_address = models.TextField(max_length=20000)
    amount_paid = models.DecimalField(max_digits=10,decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'Order - {str(self.id)}'
    
#auto add shipping date
@receiver(pre_save,sender=Order)
def set_shipped_date_on_update(sender,instance,**kwarg):
    if instance.pk:
        now = datetime.datetime.now()
        obj = sender._default_manager.get(pk=instance.pk)


        if instance.shipped and not obj.shipped:
            instance.date_shipped = now
    




#create order items model

class OrderItem(models.Model):
    #foriegnkey
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    product= models.ForeignKey(Product, on_delete=models.CASCADE,  null=True)


    quantity = models.PositiveBigIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)

    def __str__(self):
        return f'Order Item - {str(self.id)}'
    

# create a user shipping address default when they signup

def create_shipping(sender,instance,created,**kwargs):
    if created:
        user_shipping = ShippingAddress(user=instance)
        user_shipping.save()
#automate the profile thing
post_save.connect(create_shipping,sender=User)
    









