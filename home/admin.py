from django.contrib import admin
from home.models import Profile, Contact, TwoFactor, PhoneOtp, ForgotPasswordOtp

# Register your models here.
admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(TwoFactor)
admin.site.register(PhoneOtp)
admin.site.register(ForgotPasswordOtp)
