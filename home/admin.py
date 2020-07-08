from django.contrib import admin
from home.models import Profile, Contact, TwoFactor, PhoneOtp

# Register your models here.
admin.site.register(Profile)
admin.site.register(Contact)
admin.site.register(TwoFactor)
admin.site.register(PhoneOtp)
