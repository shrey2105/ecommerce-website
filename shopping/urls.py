from django.urls import path
from shopping import views

urlpatterns = [
    path("", views.index, name="shoppingHome"),
    path("about/", views.about, name="aboutUs"),
    path("contact/", views.contact, name="contactUs"),
    path("tracker/", views.tracker, name="trackingStatus"),
    path("orderTracker/", views.orderTracker, name="orderTracker"),
    path("search/", views.search, name="search"),
    path("productView/<int:id>", views.productView, name="productView"),
    path("checkout/", views.checkout, name="checkout"),
    path("paymentHandle/", views.paymentHandle, name="paymentHandle"),
    path("paymentHandleBuy/", views.paymentHandleBuy, name="paymentHandleBuy"),
    path("orderDetails/", views.orderDetails, name="orderDetails"),
    path("cartView/", views.cartView, name="cartView"),
    path("remove_from_cart/<int:id>", views.remove_from_cart, name="remove_from_cart"),
    path("add_to_cart/<int:id>", views.add_to_cart, name="add_to_cart"),
    path("buy_now/<int:id>", views.buy_now, name="buy_now"),
    path("cartCheckout/", views.cartCheckout, name="new_checkout"),
    path("cart_item_count/", views.cart_item_count, name="cart_item_count"),
    path("buy_item_count/", views.buy_item_count, name="buy_item_count")
    
]