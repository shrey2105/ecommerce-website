from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_number = models.CharField(max_length=13, blank=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, default="")
    birth_day = models.CharField(max_length=2, blank=True)
    birth_month = models.CharField(max_length=2, blank=True)
    birth_year = models.CharField(max_length=4, blank=True)
    image = models.ImageField(upload_to="home/images", default='home/images/no-profile-pic.png')
    VERIFIED_CHOICES = (
        ('VF', 'Verified'),
        ('NVF', 'Not Verified'),
    )
    is_verified = models.CharField(max_length=4, choices=VERIFIED_CHOICES, blank=True, default="NVF")
    is_email_verified = models.CharField(max_length=4, choices=VERIFIED_CHOICES, blank=True, default="NVF")

    def __str__(self):
        return self.user.username
    
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=13)
    query = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.email

class TwoFactor(models.Model):
    api_key = models.CharField(max_length=200, blank=True, null=True)
    sender_id = models.CharField(max_length=10, blank=True, null=True)
    template_name = models.CharField(max_length=30, blank=True, null=True)

    def __str__(self):
        return self.template_name

class PhoneOtp(models.Model):
    mobile_number = models.CharField(max_length=13, blank=True)
    otp = models.CharField(max_length=8, blank=True, null=True)
    count = models.IntegerField(default=1, help_text="Number of OTP sent")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return f"{str(self.otp)} is sent to {str(self.mobile_number)}" 

OTP_VERIFY_CHOICES = (
        ('VF', 'Verified'),
        ('NF', 'Not Verified'),
    )
class ForgotPasswordOtp(models.Model):
    mobile_number = models.CharField(max_length=13, blank=True)
    otp = models.CharField(max_length=8, blank=True, null=True)
    count = models.IntegerField(default=1, help_text="Number of OTP sent")
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    is_validated = models.CharField(max_length=2, choices=OTP_VERIFY_CHOICES, blank=True, default="NF")

    def __str__(self):
        return f"{str(self.otp)} is sent to {str(self.mobile_number)}" 
    


    
    
