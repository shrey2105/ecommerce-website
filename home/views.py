from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import BlogPost
from home.models import Profile
from shopping.models import Cart
import json
from django.core.files.storage import FileSystemStorage

# Create your views here.
def error_404_view(request, exception):
    return render(request, "home/404_not_found.html")

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
    if not request.user.is_authenticated:
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
            messages.success(request, "You have been successfully registered with us. Now, You can Log In")
            return redirect('/home/')
    else:
        return HttpResponseRedirect("/home")
    return render(request, "home/signup.html")

def signin(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    user = request.user
                    cart = Cart.objects.get(user=user)
                    request.session['items_total'] = cart.cartitem_set.count()
                except Cart.DoesNotExist:
                    request.session['items_total'] = 0
                messages.success(request, "Welcome to Shop N Blog! You have been logged in successfully.")
                return redirect("/home/")
            else:
                messages.error(request, "Login Failed! Kindly check your Username or Password")
                return redirect("/home/signin")
    else:
        return HttpResponseRedirect("/home")
    return render(request, "home/signin.html")


def signout(request):
    if request.user.is_authenticated:
        logout(request)
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, "home/signout.html")

def profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user_id = request.POST.get("user_id")
            user = User.objects.get(pk=user_id)
            user.first_name = request.POST.get("name")
            user.email = request.POST.get("email")
            user.profile.mobile_number = request.POST.get("mobile")
            user.profile.gender = request.POST.get("gender", False)
            user.profile.birth_day = request.POST.get("day")
            user.profile.birth_month = request.POST.get("month")
            user.profile.birth_year = request.POST.get("year")
            image = request.FILES.get("upload_image", "home/images/no-profile-pic.png")
            user.profile.image = image
            user.save()
            return HttpResponseRedirect("/home/profile")
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, "home/profile.html")

def changePassword(request):
    if request.method == "POST":
        user_id = request.POST.get("user_id")
        user = User.objects.get(pk=user_id)
        current_password_input = request.POST.get("current_password")
        verify_user = authenticate(username=user.username, password=current_password_input)
        if verify_user is not None:
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, "Password changed successfully. Kindly login again with your new password.")
            else:
                messages.error(request, "Something went wrong. Kindly check if both passwords are matching.")
        else:
            messages.error(request, "Something went wrong. Kindly check if your old password is correct.")
        return HttpResponseRedirect("/home/signin")
    return render(request, "home/profile.html")

def cannot_access(request):
    return render(request, "home/cannot_access.html")

