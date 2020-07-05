from django.contrib import admin

# Register your models here.
from shopping.models import Product, Contact, Orders, OrdersUpdate, PaytmKey, Cart, CartItem, Order, Buy, BuyItem, YoutubeLink, BannerImage

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrdersUpdate)
admin.site.register(PaytmKey)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Buy)
admin.site.register(BuyItem)
admin.site.register(BannerImage)
admin.site.register(YoutubeLink)