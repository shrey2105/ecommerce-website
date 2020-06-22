from django.urls import path
from home import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about", views.about, name="about"),
    path("search", views.search, name="search"),
    path("signup", views.signup, name="signup"),
    path("signupcheck", views.signupcheck, name="signupcheck"),
    path("passwordcheck", views.passwordcheck, name="passwordcheck"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("contact", views.contact, name="contact")
]