from django.urls import path
from blog import views

urlpatterns = [
    path("", views.index, name="blogHome"),
    path("blogPost/<int:id>", views.blogpost, name="blogPost"),
    path("postComment", views.postComment, name="postComment"),
    path("contact", views.contact, name="contact"),
    path("publish", views.publish, name="publish"),
    path("search", views.search, name="search"),
]