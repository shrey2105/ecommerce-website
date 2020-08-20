from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.

PUBLISH_STATUS_CHOICES = (
    ("Published", "Published"),
    ("Unpublished", "Unpublished"),
    ("Featured", "Featured"),
)

class BlogPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    heading1 = models.CharField(max_length=500, default="")
    content_heading1 = models.TextField()
    heading2 = models.CharField(max_length=500, default="")
    content_heading2 = models.TextField()
    sub_heading = models.CharField(max_length=500, default="")
    sub_heading_content = models.TextField()
    pub_date = models.DateField(blank=True, null=True)
    author = models.CharField(max_length=30, default="")
    thumbnail = models.ImageField(upload_to="blog/images", default="", null=True, blank=True)
    status = models.CharField(max_length=120, choices=PUBLISH_STATUS_CHOICES, default="Unpublished")

    def __str__(self):
        return self.title

class BlogComment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(default="")
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return f"{self.user} Comment is: '{self.comment[0:15]}...' on post {self.post}"

class Contact(models.Model):
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=13)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.email