from django.contrib import admin

# Register your models here.
from shopping.models import Product, Contact, Orders, OrdersUpdate, PaytmKey

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrdersUpdate)
admin.site.register(PaytmKey)