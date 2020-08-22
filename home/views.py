from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import View
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from blog.models import BlogPost
from home.models import Profile, Contact, TwoFactor, PhoneOtp, ForgotPasswordOtp
from shopping.models import Cart
import json
import requests
from home.otp import otp_key_generator
from datetime import datetime, timedelta
from django.core.mail import EmailMessage, send_mail
from home.utils import token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.safestring import mark_safe
import re
MOBILE_REGEX = re.compile(r'^[0-9]{10}$')
OTP_REGEX = re.compile(r'^[A-Z0-9]{6,6}$')
PASSWORD_REGEX = re.compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$')
msg = """
        Please note that you are not a VERIFIED USER. To verify, Click <a style='color:#000' href='{url}'><strong><em><u>Here</u></em></strong></a> to navigate to Profile Section to validate email address & mobile number and enjoy services.
    """

# Create your views here.
def error_404(request, exception):
    if request.user.is_authenticated:
        if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
            url = reverse("profile")
            messages.warning(request, mark_safe(msg.format(url=url)))
    return render(request, "home/404.html")

def error_500(request):
    if request.user.is_authenticated:
        if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
            url = reverse("profile")
            messages.warning(request, mark_safe(msg.format(url=url)))
    return render(request, "home/500.html")

def csrf_failure(request):
    if request.user.is_authenticated:
        if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
            url = reverse("profile")
            messages.warning(request, mark_safe(msg.format(url=url)))
    return render(request, "home/403_csrf.html")

def home(request):
    if request.user.is_authenticated:
        if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
            url = reverse("profile")
            messages.warning(request, mark_safe(msg.format(url=url)))
    return render(request, "home/home.html")

def about(request):
    if request.user.is_authenticated:
        if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
            url = reverse("profile")
            messages.warning(request, mark_safe(msg.format(url=url)))
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

def emailcheck(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            response = "Already in Use"
            return HttpResponse('%s' % response)
        except User.DoesNotExist:
            response = "OK"
            return HttpResponse('%s' % response)
            
    return render(request, "home/profile.html")

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
            
    return render(request, "home/profile.html")

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
            new_user.profile.credit = 2
            new_user.save()
            messages.success(request, "You have been successfully registered with us. You get Rs. 2 credits as Sign Up Bonus. Please Sign in")
            return redirect('/home/')
    else:
        return HttpResponseRedirect("/home")
    return render(request, "home/signup.html")

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            user.profile.is_email_verified = "VF"
            user.save()
            messages.success(request, 'Your Email Address has been verified.')
            return redirect('profile')
        else:
            messages.error(request, 'The confirmation link was invalid, possibly because it has already been used.')
            return redirect('profile')

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
                
                request.session['total_credits'] = float(user.profile.credit)
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
        if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
            msg_profile = """
                Please note that you are not a VERIFIED USER. To verify, please validate email address & mobile number and enjoy services.
            """
            url = reverse("profile")
            messages.warning(request, mark_safe(msg_profile.format(url=url)))
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
    return render(request, "home/profile.html", {'is_verified':login_user.profile.is_verified, 'is_email_verified':login_user.profile.is_email_verified})

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

def updateEmail(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user_id = request.POST.get("user_id")
            user = User.objects.get(pk=user_id)
            email = request.POST.get("email")
            if user.email != email:
                user.email = email
                user.save()
                messages.success(request, "Email Address Updated Successfully. Kindly verify your profile again.")
                user.profile.is_email_verified = "NVF"
                user.save()
            else:
                messages.error(request, "Can't update same Email Address.")
            return HttpResponseRedirect("/home/profile")
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, "home/profile.html")

def cannot_access(request):
    return render(request, "home/cannot_access.html")

def notVerified(request):
    if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
        url = reverse("profile")
        messages.warning(request, mark_safe(msg.format(url=url)))
    else:
        return HttpResponseRedirect("/home")
    return render(request, "home/not_verified.html")

def contact(request):
    if request.user.is_authenticated:
        if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
           url = reverse("profile")
           messages.warning(request, mark_safe(msg.format(url=url)))
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

def send_email(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = User.objects.get(pk=request.user.id)
            email = user.email
            if user.profile.is_email_verified == "NVF":

                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                domain = get_current_site(request).domain
                link = reverse("activate", kwargs={"uidb64":uidb64, "token":token_generator.make_token(user)})

                activate_url = "https://"+domain+link
                email_subject = "Activate your Shop N Blog Account"
                from_email = "Shop N Blog Support <shopnblog2020@gmail.com>"
                message = render_to_string('home/profile_activation_email.html', {
                'user': user,
                'activate_url':activate_url,
                })
                send_mail(email_subject,message,from_email,[email],fail_silently=False,html_message=message)

                return JsonResponse({'status':'success', 'message':'Email Sent. Please check your inbox for mail and click on the link to verify it.'})
            else:
                return JsonResponse({'status':'not_success', 'message':'There is some error in sending mail. Please try again.'})
            
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, "home/profile.html")

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
                            return JsonResponse({'status':'success', 'message':'OTP sent, valid for 30 minutes. Click on Verify Mobile to verify.'})
                        else:
                            return JsonResponse({'status':'not_success', 'message':'Sending OTP error, Limit exceeded. Please try after 30 minutes.'})

                except PhoneOtp.DoesNotExist:
                    old = PhoneOtp.objects.create(mobile_number=user_mobile, otp=otp)
                    old.save()
                url = f"https://2factor.in/API/R1/?module=TRANS_SMS&apikey={shop_n_blog.api_key}&to={user_mobile}&from={shop_n_blog.sender_id}&templatename={shop_n_blog.template_name}&var1={user.first_name}&var2={old.otp}"
                response = requests.request("GET", url)
                return JsonResponse({'status':'success', 'message':'OTP sent, valid for 30 minutes. Click on Verify Mobile to verify.'})
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
                    messages.success(request, "Your Mobile Number has been verified.")
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

def forgotPassword(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            shop_n_blog = TwoFactor.objects.all()[1]
            user_mobile_no = request.POST["mobile"]
            if len(user_mobile_no) < 1:
                return JsonResponse({'status':'not_success', 'message':'This is a required field and cannot be empty. Please provide mobile number.'})
            elif not MOBILE_REGEX.match(user_mobile_no):
                return JsonResponse({'status':'not_success', 'message':'Mobile number is invalid. Please provide 10 digit mobile number.'})
            else:
                profile = Profile.objects.filter(mobile_number=user_mobile_no)
                if profile.exists():
                    user = User.objects.get(pk=profile[0].user.id)
                    full_name = f"{user.first_name} {user.last_name}"
                    otp = otp_key_generator(user_mobile_no)
                    try:
                        old = ForgotPasswordOtp.objects.get(mobile_number=user_mobile_no)
                        saved_datetime = old.updated + timedelta(minutes=30)
                        currentTime = datetime.now()
                        if old.count < 2:
                            old.otp = otp
                            old.count = old.count + 1
                            old.save()
                        else:
                            if currentTime.timestamp() > saved_datetime.timestamp():
                                old.delete()
                                old = ForgotPasswordOtp.objects.create(mobile_number=user_mobile_no, otp=otp)
                                old.save()
                                url = f"https://2factor.in/API/R1/?module=TRANS_SMS&apikey={shop_n_blog.api_key}&to={user_mobile_no}&from={shop_n_blog.sender_id}&templatename={shop_n_blog.template_name}&var1={full_name}&var2={old.otp}"
                                response = requests.request("GET", url)
                                return JsonResponse({'status':'success', 'message':'OTP sent, valid for 30 minutes. Click on Enter OTP to verify.'})
                            else:
                                return JsonResponse({'status':'not_success', 'message':'Sending OTP error, Limit exceeded. Please try after 30 minutes.'})

                    except ForgotPasswordOtp.DoesNotExist:
                        old = ForgotPasswordOtp.objects.create(mobile_number=user_mobile_no, otp=otp)
                        old.save()
                    url = f"https://2factor.in/API/R1/?module=TRANS_SMS&apikey={shop_n_blog.api_key}&to={user_mobile_no}&from={shop_n_blog.sender_id}&templatename={shop_n_blog.template_name}&var1={full_name}&var2={old.otp}"
                    response = requests.request("GET", url)
                    return JsonResponse({'status':'success', 'message':'OTP sent, valid for 30 minutes. Click on Verify Mobile to verify.'})
                else:
                    return JsonResponse({'status':'not_success', 'message':'This mobile number is not registered with us. Please provide a registered mobile number.'})
    else:
        return HttpResponseRedirect("/home/signin")

    return render(request, "home/forgot_password.html")

def validateForgotPasswordOtp(request):
    if request.method == "POST":
        user_mobile_no = request.POST.get("mobile")
        user_input_otp = request.POST.get("user_otp")
        user_profile = Profile.objects.get(mobile_number=user_mobile_no)
        user = User.objects.get(pk=user_profile.user.id)
        if len(user_input_otp) < 1:
            return JsonResponse({'status':'not_success', 'message':'This is a required field and cannot be empty. Please provide OTP recieved on your mobile.'})
        elif not OTP_REGEX.match(user_input_otp):
            return JsonResponse({'status':'not_success', 'message':'OTP is invalid. Please provide 6 digit OTP recieved on your mobile.'})
        else:
            sent_otp = ForgotPasswordOtp.objects.get(mobile_number__iexact=user_mobile_no)
            if sent_otp.otp == user_input_otp:
                sent_otp.is_validated = "VF"
                sent_otp.otp = None
                sent_otp.save()
                return JsonResponse({'status':'success', 'message':'OTP verified! You can now reset your password.', 'user':user.username})
            else:
                return JsonResponse({'status':'not_success', 'message':'Wrong OTP! Not verified! You cannot reset your password. Please try again.'})
    return render(request, "home/forgot_password.html")

def resetPassword(request):
    if request.method == "POST":
        user_mobile_no = request.POST.get("mobile")
        profile = ForgotPasswordOtp.objects.get(mobile_number=user_mobile_no)
        user_profile = Profile.objects.get(mobile_number=user_mobile_no)
        user = User.objects.get(pk=user_profile.user.id)
        if profile.is_validated == "VF" and profile.otp is None:
            password1 = request.POST.get("password1")
            password2 = request.POST.get("password2")
            if len(password1) < 1 and len(password2) < 1:
                return JsonResponse({'status':'not_success', 'message':'Error! Password fields cannot be blank.'})
            elif not PASSWORD_REGEX.match(password1):
                return JsonResponse({'status':'not_success', 'message':'Password not follow the criteria. It should be 8 characters and long & should contain atleast 1 uppercase, 1 lowecase and 1 numeric. Special characters allowed.'})
            else:
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    profile.delete()
                    return JsonResponse({'status':'success', 'message':'Success! Your password successfully reset and saved. Now login with your new password.'})
                else:
                    return JsonResponse({'status':'not_success', 'message':'Failed! Not able to update your new password. Password not matched.'})
    return render(request, "home/forgot_password.html")

        

