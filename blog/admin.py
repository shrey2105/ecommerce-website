from django.contrib import admin

# Register your models here.
from blog.models import BlogPost, BlogComment, Contact, BannerImage

admin.site.register((BlogPost, BlogComment, Contact, BannerImage))

