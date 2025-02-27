from django.contrib import admin
from .models import ShippingAddress,Order,OrderItem

admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)


#create the orderitem inline
class OrderItemInline(admin.StackedInline):
    model = OrderItem
    extra = 0


#extend our order model
class OrderAdmin(admin.ModelAdmin):
    model = Order
    readonly_fields=['date_ordered']
    fields = ['user','full_name','email','shipping_address','amount_paid','date_ordered','shipped','date_shipped']
    inlines = [OrderItemInline]

#unregister the order model
admin.site.unregister(Order)

#re-register the order model
admin.site.register(Order,OrderAdmin)


