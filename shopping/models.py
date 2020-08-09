from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg, Count

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default="0")
    description = models.TextField()
    pub_date = models.DateTimeField()
    image = models.ImageField(upload_to="shopping/images", default="")
    count_sold = models.IntegerField(default=0)
    slug = models.CharField(max_length=100, blank=True, null=True)

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
    sub_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    final_total = models.DecimalField(default=10.99, max_digits=1000, decimal_places=2)
    name = models.CharField(max_length=100, default="")
    email = models.CharField(max_length=100, default="")
    address1 = models.CharField(max_length=100, default="")
    address2 = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    zip_code = models.CharField(max_length=100, default="")
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
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.update_description[0:]

class PaytmKey(models.Model):
    name = models.CharField(max_length=50, default="", blank=True, null=True)
    merchant_id = models.CharField(max_length=50, default="", blank=True, null=True)
    merchant_key = models.CharField(max_length=50, default="", blank=True, null=True)

    def __str__(self):
        return self.name

class BannerImage(models.Model):
    image_url = models.ImageField(upload_to="shopping/images", blank=True, null=True)
    second_image_url = models.ImageField(upload_to="shopping/images", blank=True, null=True)
    third_image_url = models.ImageField(upload_to="shopping/images", blank=True, null=True)

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



