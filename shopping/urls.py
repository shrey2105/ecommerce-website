from django.urls import path
from shopping import views

urlpatterns = [
    path("", views.index, name="shoppingHome"),
    path("contact/", views.contact, name="contactUs"),
    path("tracker/", views.tracker, name="trackingStatus"),
    path("orderTracker/", views.orderTracker, name="orderTracker"),
    path("search/", views.search, name="search"),
    path("productView/<int:id>", views.productView, name="productView"),
    path("paymentHandle/", views.paymentHandle, name="paymentHandle"),
    path("paymentHandleBuy/", views.paymentHandleBuy, name="paymentHandleBuy"),
    path("orderDetails/", views.orderDetails, name="orderDetails"),
    path("cartView/", views.cartView, name="cartView"),
    path("paymentMethod/", views.paymentMethod, name="paymentMethod"),
    path("remove_from_cart/<int:id>", views.remove_from_cart, name="remove_from_cart"),
    path("add_to_cart/<int:id>", views.add_to_cart, name="add_to_cart"),
    path("itemCheckout/<int:id>", views.buy_now, name="buy_now"),
    path("cartCheckout/", views.cartCheckout, name="new_checkout"),
    path("cart_item_count/", views.cart_item_count, name="cart_item_count"),
    path("buy_item_count/", views.buy_item_count, name="buy_item_count"),
    path("review/<slug:url>", views.review, name="review"),
    path("creditProcess/", views.creditProcess, name="creditProcess"),
    path("codProcess/", views.codProcess, name="codProcess"),
]