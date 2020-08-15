from django.urls import path
from home import views
from home.views import VerificationView

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("signup", views.signup, name="signup"),
    path("signupcheck", views.signupcheck, name="signupcheck"),
    path("mobilecheck", views.mobilecheck, name="mobilecheck"),
    path("emailcheck", views.emailcheck, name="emailcheck"),
    path("signin", views.signin, name="signin"),
    path("signout", views.signout, name="signout"),
    path("profile", views.profile, name="profile"),
    path("changePassword", views.changePassword, name="changePassword"),
    path("updateMobile", views.updateMobile, name="updateMobile"),
    path("updateEmail", views.updateEmail, name="updateEmail"),
    path("cannot_access", views.cannot_access, name="cannot_access"),
    path("contact", views.contact, name="contact"),
    path("send_otp", views.send_otp, name="send_otp"),
    path("send_email", views.send_email, name="send_email"),
    path("validateOtp", views.validateOtp, name="validateOtp"),
    path("notVerified", views.notVerified, name="notVerified"),
    path("forgotPassword", views.forgotPassword, name="forgotPassword"),
    path("validateForgotPasswordOtp", views.validateForgotPasswordOtp, name="validateForgotPasswordOtp"),
    path("resetPassword", views.resetPassword, name="resetPassword"),
    path("activate/<uidb64>/<token>", VerificationView.as_view(), name="activate")
]