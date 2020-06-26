from django.urls import path
from shopping import views

urlpatterns = [
    path("", views.index, name="shoppingHome"),
    path("about/", views.about, name="aboutUs"),
    path("contact/", views.contact, name="contactUs"),
    path("tracker/", views.tracker, name="trackingStatus"),
    path("search/", views.search, name="search"),
    path("productView/<int:id>", views.productView, name="productView"),
    path("checkout/", views.checkout, name="checkout"),
    path("emptyCart/", views.emptyCart, name="emptyCart"),
    path("paymentHandle/", views.paymentHandle, name="paymentHandle"),
    path("orderDetails/", views.orderDetails, name="orderDetails")
]