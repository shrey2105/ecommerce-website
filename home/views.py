from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.models import Contact
from blog.models import BlogPost
import json

# Create your views here.
def home(request):
	return render(request, "home/home.html")

def contact(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            mobile = request.POST.get("mobile")
            message = request.POST.get("message")
            contact = Contact(name=name, email=email, mobile=mobile, message=message)
            contact.save()
            response = json.dumps({"status": "success"})
            return HttpResponse(response)
        except Exception as e:
            response = json.dumps({"status": "failure"})
            return HttpResponse(response)
        # messages.success(request, "Your response has been successfully recorded."
    return render(request, "home/contact.html")

def about(request):
    return render(request, "home/about.html")

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

def passwordcheck(request):
    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        try:
            if password1 == password2 and password1 != "" and password2 != "":
                response = "OK"
            else:
                response = "Mot Match"
            # return HttpResponse('%s' % response)
            print(response)
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
        return redirect('/blog/')
    return render(request, "home/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Welcome to Devastator Blogs! You have been logged in successfully")
            return redirect("/blog/")
        else:
            messages.error(request, "Login Failed! Kindly check your Username or Password")
            return redirect("/blog/signin")
    return render(request, "home/signin.html")


def signout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out! Thank You")
    return redirect("/blog/")
    return render(request, "home/signout.html")
