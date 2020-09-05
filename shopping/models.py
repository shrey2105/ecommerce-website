from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
import requests
import json
import paytmchecksum

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=300)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    description = models.TextField()
    pub_date = models.DateTimeField()
    stock_qty = models.PositiveIntegerField()
    image = models.ImageField(upload_to="shopping/images")
    count_sold = models.IntegerField(default=0)
    slug = models.CharField(max_length=300, blank=True, null=True)

    def __str__(self):
        return self.product_name

    def averageRating(self):
        reviews = Comment.objects.filter(product=self).aggregate(average=Avg('rating'))
        avg = 0
        if reviews["average"] is not None:
            avg = float(reviews["average"])
        return avg

    def reviewCount(self):
        reviews = Comment.objects.filter(product=self).aggregate(count=Count('id'))
        cnt = 0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt

    def save(self, *args, **kwargs):
        try:
            wishlist_item = WishlistItem.objects.filter(product=self.id)
            for item in wishlist_item:
                email = item.user.email
                email_subject = "Your Item is Back on Shop N Blog"
                from_email = "Shop N Blog Support <shopnblog2020@gmail.com>"
                message = render_to_string('shopping/wishlist_email.html', {
                    'user': item.user,
                    'product_name':item.product.product_name,
                    'product_image':item.product.image.url,
                    'product_price':item.product.price,
                })
                send_mail(email_subject,message,from_email,[email],fail_silently=False,html_message=message)
                wishlist = Wishlist.objects.get(user=item.user)
                wishlist.delete()
        except Exception as e:
            print(e)
        super(Product, self).save(*args, **kwargs)

class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    wishlist = models.ForeignKey('Wishlist', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        try:
            return f"{self.wishlist.id}"
        except:
            return self.product.product_name

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Wishlist id: {self.id}"

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        try:
            return f"{self.cart.id}"
        except:
            return self.product.product_name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart id: {self.id}"

class BuyItem(models.Model):
    buy = models.ForeignKey('Buy', on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    line_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        try:
            return f"{self.buy.id}"
        except:
            return self.product.product_name

class Buy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    total_price = models.DecimalField(max_digits=100, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Buy id: {self.id}"
    
class Contact(models.Model):
    query_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=60, default="")
    mobile = models.CharField(max_length=60, default="")
    query_message = models.CharField(max_length=500, default="")

    def __str__(self):
        return self.name

STATUS_CHOICES = (
    ("Started", "Started"),
    ("Abandoned", "Abandoned"),
    ("Return", "Return"),
    ("Finished", "Finished"),
)
ORDER_STATUS_CHOICES = (
    ("Delivered", "Delivered"),
    ("Not Delivered", "Not Delivered"),
)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    order_id = models.CharField(max_length=120, default='ABC', unique=True)
    cartproduct_items = models.CharField(max_length=5000, null=True, blank=True, default="")
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True)
    buy = models.ForeignKey(Buy, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, default="Started")
    order_status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default="Not Delivered")
    credits_used = models.DecimalField(default=0.00, max_digits=1000, decimal_places=2, blank=True, null=True)
    final_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    transaction_id = models.CharField(default="0", blank=True, null=True, max_length=100)
    reference_id = models.CharField(default="0", blank=True, null=True, max_length=50)
    payment_mode = models.CharField(default="0", blank=True, null=True, max_length=100)
    is_amount_paid = models.BooleanField(default=False, blank=True, null=True)
    name = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="")
    address1 = models.CharField(max_length=100, default="")
    address2 = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    zip_code = models.CharField(max_length=100, default="")
    post_office = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=50, default="")
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.order_id)

class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    mobile_number = models.CharField(max_length=50, default="")
    total_price = models.IntegerField(default=0) 

    def __str__(self):
        return self.name      

class OrdersUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.CharField(max_length=20, default="")
    update_description = models.CharField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.order_id}: {self.update_description[0:]}"

    def save(self, *args, **kwargs):
        try:
            order_update = Order.objects.get(order_id=self.order_id)
            if self.update_description == "Delivered":
                order_update.order_status = "Delivered"
                order_update.is_amount_paid = True
                order_update.save()
            elif self.update_description == "Returned":
                if order_update.payment_mode == "paytm":
                    paytmParams = dict()
                    paytmParams["body"] = {
                        "mid"          : settings.MERCHANT_ID,
                        "txnType"      : "REFUND",
                        "orderId"      : order_update.order_id,
                        "txnId"        : order_update.transaction_id,
                        "refId"        : order_update.reference_id,
                        "refundAmount" : str(order_update.final_total),
                    }
                    checksum = paytmchecksum.generateSignature(json.dumps(paytmParams["body"]), settings.MERCHANT_KEY)
                    paytmParams["head"] = {
                        "signature"    : checksum
                    }
                    post_data = json.dumps(paytmParams)
                    # for Staging
                    url = "https://securegw-stage.paytm.in/refund/apply"
                    # for Production
                    # url = "https://securegw.paytm.in/refund/apply"
                    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"})
                    r = response.json()
                    if r['body']['resultInfo']['resultCode'] == "601" or r['body']['resultInfo']['resultCode'] == "617":
                        order_update.status = "Abandoned"
                        order_update.save()
                
                elif order_update.payment_mode == "credits":
                    order_update.status = "Abandoned"
                    order_update.save()
                    user.profile.credit = float(order_update.credits_used)
                    user.save()
                    request.session['total_credits'] = user.profile.credit

                elif order_update.payment_mode == "cod":
                    order_update.status = "Abandoned"
                    order_update.save()

                elif order_update.payment_mode == "credits + paytm":
                    remaining_amount = 0.0
                    user = User.objects.get(pk=order_update.user.id)
                    user.profile.credit = float(order_update.credits_used)
                    remaining_amount = float(order_update.final_total) - float(order_update.credits_used)
                    paytmParams = dict()
                    paytmParams["body"] = {
                        "mid"          : settings.MERCHANT_ID,
                        "txnType"      : "REFUND",
                        "orderId"      : order_update.order_id,
                        "txnId"        : order_update.transaction_id,
                        "refId"        : order_update.reference_id,
                        "refundAmount" : str(remaining_amount),
                    }
                    checksum = paytmchecksum.generateSignature(json.dumps(paytmParams["body"]), settings.MERCHANT_KEY)
                    paytmParams["head"] = {
                        "signature"    : checksum
                    }
                    post_data = json.dumps(paytmParams)
                    # for Staging
                    url = "https://securegw-stage.paytm.in/refund/apply"
                    # for Production
                    # url = "https://securegw.paytm.in/refund/apply"
                    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"})
                    r = response.json()
                    if r['body']['resultInfo']['resultCode'] == "601" or r['body']['resultInfo']['resultCode'] == "617":
                        order_update.status = "Abandoned"
                        order_update.save()
                        user.save()
        except Exception as e:
            print(e)
        super(OrdersUpdate, self).save(*args, **kwargs)  

class BannerImage(models.Model):
    image_url = models.ImageField(upload_to="shopping/images", blank=True, null=True)
    second_image_url = models.ImageField(upload_to="shopping/images", blank=True, null=True)
    third_image_url = models.ImageField(upload_to="shopping/images", blank=True, null=True)
    fourth_image_url = models.ImageField(upload_to="shopping/images", blank=True, null=True)

    def __str__(self):
        return f"Banner Image id:{self.id}"

class YoutubeLink(models.Model):
    youtube_video_link = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return f"Youtube Link id:{self.id}"

class Comment(models.Model):
    STATUS_CHOICES = (
    ("New", "New"), 
    ("True", "True"),
    ("False", "False"),
)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True, null=True)
    comment = models.CharField(max_length=300, blank=True, null=True)
    rating = models.IntegerField(default=1, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="New")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment: {self.comment} on Product: {self.product}"




