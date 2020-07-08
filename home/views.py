from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from blog.models import BlogPost
from home.models import Profile, Contact, TwoFactor, PhoneOtp
from shopping.models import Cart
import json
import requests
from home.otp import otp_key_generator
from datetime import datetime, timedelta


# Create your views here.
def error_404(request, exception):
    return render(request, "home/404.html")

def error_500(request):
    return render(request, "home/500.html")

def csrf_failure(request):
    return render(request, "home/403_csrf.html")

def home(request):
	return render(request, "home/home.html")

def about(request):
    return render(request, 'home/about.html')

def signupcheck(request):
    if request.method == "POST":
        username = request.POST.get("username")
        try:
            user = User.objects.get(username=username)
            response = "Already in Use"
            return HttpResponse('%s' % response)
        except User.DoesNotExist:
            response = "OK"
            return HttpResponse('%s' % response)
            
    return render(request)

def mobilecheck(request):
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        try:
            profile = Profile.objects.get(mobile_number=mobile)
            response = "Already in Use"
            return HttpResponse('%s' % response)
        except Profile.DoesNotExist:
            response = "OK"
            return HttpResponse('%s' % response)
            
    return render(request)

def signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get("username")
            firstname= request.POST.get("firstname")
            lastname= request.POST.get("lastname")
            email = request.POST.get("email")
            mobile = request.POST.get("mobile")
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            day = request.POST.get("day")
            month = request.POST.get("month")
            year = request.POST.get("year")
            gender = request.POST.get("gender", False)
                
            user = User.objects.create_user(username, email, password1)
            user.save()
            new_user = User.objects.get(pk=user.id)
            new_user.first_name = firstname
            new_user.last_name = lastname
            new_user.profile.mobile_number = mobile
            new_user.profile.birth_day = day
            new_user.profile.birth_month = month
            new_user.profile.birth_year = year
            new_user.profile.gender = gender
            new_user.save()
            messages.success(request, "You have been successfully registered with us. Now, You can Log In.")
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
                if request.user.profile.is_verified == "NVF":
                    messages.warning(request, "Please note that you are not a VERIFIED USER. To verify, navigate to profile section to validate mobile number and enjoy services.")
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
        login_user = User.objects.get(pk=request.user.id)

        if request.method == "POST":
            user_id = request.POST.get("user_id")
            user = User.objects.get(pk=user_id)
            user.first_name = request.POST.get("name")
            user.email = request.POST.get("email")
            user.profile.gender = request.POST.get("gender", False)
            user.profile.birth_day = request.POST.get("day")
            user.profile.birth_month = request.POST.get("month")
            user.profile.birth_year = request.POST.get("year")
            image = request.FILES.get("upload_image", "home/images/no-profile-pic.png")
            user.profile.image = image
            user.save()
            messages.success(request, "Profile updated successfully.")
            return HttpResponseRedirect("/home/profile")
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, "home/profile.html", {'is_verified':login_user.profile.is_verified})

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
                return HttpResponseRedirect("/home/signin")
            else:
                messages.error(request, "Something went wrong. Kindly check if both passwords are matching.")
                return HttpResponseRedirect("/home/profile")
        else:
            messages.error(request, "Something went wrong. Kindly check if your old password is correct.")
            return HttpResponseRedirect("/home/profile")
    return render(request, "home/profile.html")

def updateMobile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user_id = request.POST.get("user_id")
            user = User.objects.get(pk=user_id)
            mobile = request.POST.get("mobile")
            if user.profile.mobile_number != mobile:
                user.profile.mobile_number = mobile
                user.save()
                messages.success(request, "Mobile Number Updated Successfully. Kindly verify your profile again.")
                user.profile.is_verified = "NVF"
                user.save()
            else:
                messages.error(request, "Can't update same Mobile Number.")
            return HttpResponseRedirect("/home/profile")
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, "home/profile.html")

def cannot_access(request):
    return render(request, "home/cannot_access.html")

def notVerified(request):
    return render(request, "home/not_verified.html")

def contact(request):
    if request.method == "POST":
        try:
            name = request.POST.get("name")
            email = request.POST.get("email")
            mobile = request.POST.get("mobile")
            message = request.POST.get("message")
            contact = Contact(name=name, email=email, mobile=mobile, query=message)
            contact.save()
            response = json.dumps({"status": "success"})
            return HttpResponse(response)
        except Exception as e:
            response = json.dumps({"status": "failure"})
            return HttpResponse(response)
    return render(request, "home/contact.html")

def send_otp(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            shop_n_blog = TwoFactor.objects.all()[0]
            user = User.objects.get(pk=request.user.id)
            user_mobile = request.POST.get("mobile")
            if user.profile.is_verified == "NVF":
                otp = otp_key_generator(user_mobile)
                try:
                    old = PhoneOtp.objects.get(mobile_number=user_mobile)
                    saved_datetime = old.updated + timedelta(minutes=30)
                    currentTime = datetime.now()
                    if old.count < 2:
                        old.otp = otp
                        old.count = old.count + 1
                        old.save()
                    else:
                        if currentTime.timestamp() > saved_datetime.timestamp():
                            old.delete()
                            old = PhoneOtp.objects.create(mobile_number=user_mobile, otp=otp)
                            old.save()
                            url = f"https://2factor.in/API/R1/?module=TRANS_SMS&apikey={shop_n_blog.api_key}&to={user_mobile}&from={shop_n_blog.sender_id}&templatename={shop_n_blog.template_name}&var1={user.first_name}&var2={old.otp}"
                            response = requests.request("GET", url)
                            return JsonResponse({'status':'success', 'message':'OTP sent, valid for 30 minutes. Click on Verify Mobile to enter recieved OTP.'})
                        else:
                            return JsonResponse({'status':'not_success', 'message':'Sending OTP error, Limit exceeded. Please try after 30 minutes.'})

                except PhoneOtp.DoesNotExist:
                    old = PhoneOtp.objects.create(mobile_number=user_mobile, otp=otp)
                    old.save()
                url = f"https://2factor.in/API/R1/?module=TRANS_SMS&apikey={shop_n_blog.api_key}&to={user_mobile}&from={shop_n_blog.sender_id}&templatename={shop_n_blog.template_name}&var1={user.first_name}&var2={old.otp}"
                response = requests.request("GET", url)
                return JsonResponse({'status':'success', 'message':'OTP sent, valid for 30 minutes. Click on Verify Mobile to enter recieved OTP.'})
            else:
                return JsonResponse({'status':'error'})
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, "home/profile.html")

def validateOtp(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user_mobile_no = request.POST.get("validation_otp_mobile")
            user_input_otp = request.POST.get("user_otp")
            user = User.objects.get(pk=request.user.id)
            if user.profile.is_verified == "NVF":
                sent_otp = PhoneOtp.objects.get(mobile_number__iexact=user_mobile_no)
                if sent_otp.otp == user_input_otp:
                    user.profile.is_verified = "VF"
                    user.save()
                    messages.success(request, "OTP verified! Your profile status is now verified.")
                    sent_otp.delete()
                    return HttpResponseRedirect("/home/profile")
                else:
                    messages.warning(request, "OTP is invalid. Dosen't matched.")
                    return HttpResponseRedirect("/home/profile")
            else:
                messages.warning(request, "Profile status already verified.")
                return HttpResponseRedirect("/home/profile")
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, "home/profile.html")

