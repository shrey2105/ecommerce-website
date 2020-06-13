from django.shortcuts import render
from .models import BlogPost

# Create your views here.
def index(request):
	blogposts = BlogPost.objects.all()
	params = {'blogposts':blogposts}
	return render(request, 'blog/index.html', params)

def blogpost(request, id):
	blogpost = BlogPost.objects.filter(post_id=id)
	params = {'blogpost':blogpost[0]}
	return render(request, 'blog/blogpost.html', params)