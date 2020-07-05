from django.urls import path
from home import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("signup", views.signup, name="signup"),
    path("signupcheck", views.signupcheck, name="signupcheck"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("profile", views.profile, name="profile"),
    path("changePassword", views.changePassword, name="changePassword"),
    path("cannot_access", views.cannot_access, name="cannot_access"),
    path("contact", views.contact, name="contact"),
]