from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import BlogPost
import json

# Create your views here.
def home(request):
	return render(request, "home/home.html")

def search(request):
    query = request.GET.get("query")
    if len(query) > 60:
        all_posts = BlogPost.objects.none()
    else:
        all_posts_title = BlogPost.objects.filter(title__icontains=query)
        all_posts_content = BlogPost.objects.filter(content_heading1__icontains=query)
        all_posts = all_posts_title.union(all_posts_content)
    params = {'all_posts':all_posts, 'message':''}
    if len(all_posts) == 0 or len(query) <= 1:
        params = {'message':'Search Not Found, Search again...'}
    return render(request, "home/search.html", params)

def signupcheck(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = User.objects.filter(username=username)
            if user.count() > 0:
                response = "Already in Use"     
            else:
                response = "OK"
            return HttpResponse('%s' % response)

        except Exception as e:
            return HttpResponse("error")
            
    return render(request)

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        firstname= request.POST.get("firstname")
        lastname= request.POST.get("lastname")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
            
        user = User.objects.create_user(username, email, password1)
        user.first_name = firstname
        user.last_name = lastname
        user.save()
        messages.success(request, "You have been successfully registered with us")
        return redirect('/home/')
    return render(request, "home/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome to Devastator Blogs! You have been logged in successfully")
            return redirect("/home/")
        else:
            messages.error(request, "Login Failed! Kindly check your Username or Password")
            return redirect("/home/signin")
    return render(request, "home/signin.html")


def signout(request):
    logout(request)
    return render(request, "home/signout.html")
