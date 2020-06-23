from django.contrib import admin

# Register your models here.
from blog.models import BlogPost, BlogComment, Contact

admin.site.register((BlogPost, BlogComment, Contact))

