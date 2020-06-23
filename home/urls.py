from django.urls import path
from home import views

urlpatterns = [
    path("", views.home, name="home"),
    path("search", views.search, name="search"),
    path("signup", views.signup, name="signup"),
    path("signupcheck", views.signupcheck, name="signupcheck"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
]