from django.db import models

# Create your models here.
class BlogPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    heading1 = models.CharField(max_length=500, default="")
    content_heading1 = models.CharField(max_length=5000, default="")
    heading2 = models.CharField(max_length=500, default="")
    content_heading2 = models.CharField(max_length=5000, default="")
    sub_heading = models.CharField(max_length=500, default="")
    sub_heading_content = models.CharField(max_length=5000, default="")
    pub_date = models.DateField()
    thumbnail = models.ImageField(upload_to="blog/images", default="")

    def __str__(self):
        return self.title