from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from shopping.models import Product, Contact, Orders, Cart, CartItem, Order, OrdersUpdate, Buy, BuyItem, BannerImage, YoutubeLink, Comment
from django.contrib import messages
from django.contrib.auth.models import User
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTM import Checksum
from django.urls import reverse
from .utils import orderid_generator
import ast
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, timedelta
from django.utils.safestring import mark_safe
from django.conf import settings
from decimal import *
from datetime import datetime, timedelta
import requests
import re
PINCODE_REGEX = re.compile(r'^[0-9]{6,6}$')
msg = """
        Please note that you are not a VERIFIED USER. To verify, Click <a style='color:#000' href='{url}'><strong><em><u>Here</u></em></strong></a> to navigate to Profile Section to validate email address & mobile number and enjoy services.
    """
    
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        request.session['total_credits'] = float(request.user.profile.credit)
        if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
            url = reverse("profile")
            messages.warning(request, mark_safe(msg.format(url=url)))
    all_products = []
    latest_products = []
    trending_products = []
    total_products_count = 0
    total_members_count = 0

    total_members = User.objects.all()
    for members in total_members:
        if not members.is_staff:
            total_members_count += 1

    total_products_redemption = Product.objects.all().order_by('count_sold', 'id')
    for total_products in total_products_redemption:
        if total_products.count_sold > 0:
            total_products_count = total_products_count + total_products.count_sold

    all_trending_products = Product.objects.all().order_by('-count_sold', '-id')[:10]
    for top_products in all_trending_products:
        if top_products.count_sold > 0:
            trending_products.append(top_products)

    all_latest_products = Product.objects.all().order_by('-pub_date', '-id')[:10]
    for products in all_latest_products:
        saved_datetime = products.pub_date + timedelta(days=30)
        currentTime = datetime.now()
        if currentTime.timestamp() < saved_datetime.timestamp():
            latest_products.append(products)

    product_category = Product.objects.values('category','id').order_by('category', 'id')
    categories = {item['category'] for item in product_category}
    for category in categories:
        prod = Product.objects.filter(category = category).order_by('category')
        n = len(prod)
        no_slides = n // 4 + ceil((n / 4) - (n // 4))
        all_products.append([prod, range(1, no_slides), no_slides])
    
    page = request.GET.get('page', 1)

    paginator = Paginator(all_products, 4)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)

    banner_image = BannerImage.objects.all()
    youtube_link = YoutubeLink.objects.all()[0]
    params = {'all_products':all_products, 'banner':banner_image, 'youtube':youtube_link, 'all_latest_products':latest_products, 'all_trending_products':trending_products,
    'total_products_count':total_products_count, 'total_members_count':total_members_count, 'records':records}
    return render(request, 'shopping/index.html', params)

def contact(request):
    if request.user.is_authenticated:
        request.session['total_credits'] = float(request.user.profile.credit)
        if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
            url = reverse("profile")
            messages.warning(request, mark_safe(msg.format(url=url)))
    if request.method == 'POST':
        try:
            name = request.POST.get("name", default="")
            email = request.POST.get("email", default="")
            mobile = request.POST.get("mobile", default="")
            query_message = request.POST.get("query_message", default="")
            contact = Contact(name=name, email=email, mobile=mobile, query_message=query_message)
            contact.save()
            response = json.dumps({"status": "success"})
            return HttpResponse(response)
        # messages.success(request, "Your response has been successfully recorded.")
        except Exception as e:
            response = json.dumps({"status": "failure"})
            return HttpResponse(response)
    return render(request, 'shopping/contact.html')

def tracker(request):
    if request.method == 'POST':
        orderid = request.POST.get("orderid", default="")
        email = request.POST.get("email", default="")
        
        try:
            order = Orders.objects.filter(order_id=orderid)
            if len(order) > 0:
                update = OrdersUpdate.objects.filter(order_id=orderid)
                updates = []
                for item in update:
                    updates.append({'text':item.update_description, 'time':item.timestamp})
                    response = json.dumps({"status":"success", "updates":updates, "items_json":order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')

        except Exception as e:
            return HttpResponse('{"status":"error"}')

    return render(request, 'shopping/tracker.html')

def orderTracker(request):
    if request.user.is_authenticated:
        request.session['total_credits'] = float(request.user.profile.credit)
        if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
            url = reverse("profile")
            messages.warning(request, mark_safe(msg.format(url=url)))
        if request.user.profile.is_verified == "VF" and request.user.profile.is_email_verified == "VF":
            if request.method == 'POST':
                orderid = request.POST.get("orderid", default="")
                
                try:
                    order = Order.objects.filter(order_id=orderid, user=request.user)
                    if len(order) > 0:
                        update = OrdersUpdate.objects.filter(order_id=orderid)
                        updates = []
                        for item in update:
                            updates.append({'text':item.update_description, 'time':item.created_at.strftime("%A, %B %d, %Y %I:%M %p")})
                            response = json.dumps({"status":"success", "updates":updates, "items_json":order[0].cartproduct_items}, default=str)
                        return HttpResponse(response)
                    else:
                        return HttpResponse('{"status":"noitem"}')

                except Exception as e:
                    return HttpResponse('{"status":"error"}')
        else:
            return HttpResponseRedirect("/home/notVerified")
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, 'shopping/new_tracker.html')

def searchMatch(query, item):
    if query in item.product_name.lower() or query in item.category.lower() or query in item.description.lower():
        return True
    else:
        return False

def search(request):
    if request.user.is_authenticated:
        request.session['total_credits'] = float(request.user.profile.credit)
        if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
            url = reverse("profile")
            messages.warning(request, mark_safe(msg.format(url=url)))
    query = request.GET.get("search")
    all_products = []
    product_category = Product.objects.values('category','id')
    categories = {item['category'] for item in product_category}
    for category in categories:
        prod = Product.objects.filter(category = category)
        products = [item for item in prod if searchMatch(query, item)]
        n = len(prod)
        no_slides = n // 4 + ceil((n / 4) - (n // 4))
        if len(products) > 0:
            all_products.append([products, range(1, no_slides), no_slides])
    params = {'all_products':all_products, 'message':''}
    if len(all_products) == 0 or len(query) <= 1:
        params = {'message':'Search Not Found, Search again...'}
    return render(request, 'shopping/search.html', params)

def productView(request, id):
    if request.user.is_authenticated:
        request.session['total_credits'] = float(request.user.profile.credit)
        if request.user.profile.is_verified == "NVF" or request.user.profile.is_email_verified == "NVF":
            url = reverse("profile")
            messages.warning(request, mark_safe(msg.format(url=url)))
    #Fetching product using id
    product = Product.objects.get(id = id)
    comments = Comment.objects.filter(product=product).order_by('-id')

    page = request.GET.get('page', 1)

    paginator = Paginator(comments, 3)
    try:
        records = paginator.page(page)
    except PageNotAnInteger:
        records = paginator.page(1)
    except EmptyPage:
        records = paginator.page(paginator.num_pages)
    params = {'product':product, 'records':records, 'user':request.user}
    return render(request, 'shopping/product_view.html', params)

def cartCheckout(request):
    request.session['total_credits'] = float(request.user.profile.credit)
    if request.user.profile.is_verified == "VF" and request.user.profile.is_email_verified == "VF":
        thanks = request.POST.get("buy_thanks")
        if thanks:
            try:
                user = request.user
                buy = Buy.objects.get(user=user)
                buy_item = BuyItem.objects.filter(buy=buy.id)
                
                items = []
                for item in buy_item:
                    items.append([item.product.product_name, item.quantity, item.product.slug, item.product.image.url])
            except:
                return HttpResponseRedirect(reverse("new_checkout"))
            
            if request.method == "POST":
                name = request.POST.get("name", default="")
                email = request.POST.get("email", default="")
                address1 = request.POST.get("address1", default="")
                address2 = request.POST.get("address2", default="")
                city = request.POST.get("city1", default="")
                state = request.POST.get("state1", default="")
                zip_code = request.POST.get("zip_code", default="")
                mobile_number = request.POST.get("mobile_number", default="")
                post_office = request.POST.get("post_office", default="")

                try:
                    new_order = Order.objects.get(buy=buy)
                except Order.DoesNotExist:
                    new_order = Order()
                    new_order.buy = buy
                    new_order.Cart = None
                    new_order.user = request.user
                    new_order.order_id = orderid_generator()
                    new_order.cartproduct_items = items
                    new_order.final_total = buy.total_price
                    new_order.name = name
                    new_order.email = email
                    new_order.address1 = address1
                    new_order.address2 = address2
                    new_order.city = city
                    new_order.state = state
                    new_order.zip_code = zip_code
                    new_order.mobile_number = mobile_number
                    new_order.post_office = post_office
                    new_order.save()
                except:
                    return HttpResponseRedirect(reverse("new_checkout"))

                orders_update = OrdersUpdate(order_id=new_order.order_id, update_description="Your order has been placed") 
                orders_update.save()

                return render(request, "shopping/payment_method.html", {'final_price':buy.total_price, 'credits':user.profile.credit, 'buy_thanks':thanks})
            return render(request, "shopping/new_checkout.html", {'buy_item':buy_item, 'buy_total':buy.total_price})

        else:
            try:
                user = request.user
                cart = Cart.objects.get(user=user)
                cart_item = CartItem.objects.filter(cart=cart.id)
                items = []
                for item in cart_item:
                    items.append([item.product.product_name, item.quantity, item.product.slug, item.product.image.url])
            except:
                return HttpResponseRedirect(reverse("cartView"))

            if request.method == "POST":
                name = request.POST.get("name", default="")
                email = request.POST.get("email", default="")
                address1 = request.POST.get("address1", default="")
                address2 = request.POST.get("address2", default="")
                city = request.POST.get("city1", default="")
                state = request.POST.get("state1", default="")
                zip_code = request.POST.get("zip_code", default="")
                mobile_number = request.POST.get("mobile_number", default="")
                post_office = request.POST.get("post_office", default="")

                try:
                    new_order = Order.objects.get(cart=cart)
                except Order.DoesNotExist:
                    new_order = Order()
                    new_order.cart = cart
                    new_order.buy = None
                    new_order.user = request.user
                    new_order.order_id = orderid_generator()
                    new_order.cartproduct_items = items
                    new_order.final_total = cart.total_price
                    new_order.name = name
                    new_order.email = email
                    new_order.address1 = address1
                    new_order.address2 = address2
                    new_order.city = city
                    new_order.state = state
                    new_order.zip_code = zip_code
                    new_order.mobile_number = mobile_number
                    new_order.post_office = post_office
                    new_order.save()
                except:
                    return HttpResponseRedirect(reverse("cartview"))

                orders_update = OrdersUpdate(order_id=new_order.order_id, update_description="Your order has been placed") 
                orders_update.save()
                
                return render(request, "shopping/payment_method.html", {'final_price':cart.total_price, 'credits':user.profile.credit})
            return render(request, "shopping/new_checkout.html", {'cart_item':cart_item, 'cart_total':cart.total_price})
    else:
        return HttpResponseRedirect("/home/notVerified")
    return render(request, "shopping/new_checkout.html")

def paymentMethod(request):
    if request.user.is_authenticated:
        request.session['total_credits'] = float(request.user.profile.credit)
        thanks = request.POST.get("buy_thanks")
        if thanks:
            try:
                user = request.user
                buy = Buy.objects.get(user=user)
                buy_item = BuyItem.objects.filter(buy=buy.id)
                new_order = Order.objects.get(buy=buy)
            except:
                return HttpResponseRedirect("/shop/cartCheckout")

            if request.method == "POST":
                payment_type = request.POST.get("payment")

                if payment_type == "paytm":
                    # After payment, request paytm to transfer amount to our account done by customer
                    params_dict = {
                        'MID':settings.MERCHANT_ID,
                        'ORDER_ID':new_order.order_id,
                        'TXN_AMOUNT':str(buy.total_price),
                        'CUST_ID':user.email,
                        'INDUSTRY_TYPE_ID':'Retail',
                        'WEBSITE':settings.WEBSITE,
                        'CHANNEL_ID':'WEB',
                        'CALLBACK_URL':'http://127.0.0.1:8000/shop/paymentHandleBuy/',
                        'MERC_UNQ_REF':str(user.id),
                    }
                    params_dict['CHECKSUMHASH'] = Checksum.generate_checksum(params_dict, settings.MERCHANT_KEY)
                    return render(request, 'shopping/paytm.html', {'params_dict':params_dict})

                elif payment_type == "credits":
                    now = datetime.now()
                    dt_string = now.strftime("%A, %B %d, %Y %I:%M %p")

                    params_dict = {
                        'credits':user.profile.credit,
                        'user':str(user.id),
                        'buy':buy,
                        'buy_item':buy_item,
                        'new_order':new_order,
                        'total_price':buy.total_price,
                        'txn_date':dt_string,
                        'payment':True,
                        'process':'buy',
                        }     
                    return render(request, "shopping/credits.html", {'params_dict':params_dict})
                
                else:
                    now = datetime.now()
                    dt_string = now.strftime("%A, %B %d, %Y %I:%M %p")

                    params_dict = {
                        'credits':user.profile.credit,
                        'user':str(user.id),
                        'buy':buy,
                        'buy_item':buy_item,
                        'new_order':new_order,
                        'total_price':buy.total_price,
                        'txn_date':dt_string,
                        'cod':True,
                        'process':'buy',
                        }     
                    return render(request, "shopping/cod.html", {'params_dict':params_dict})
        else:
            try:
                user = request.user
                cart = Cart.objects.get(user=user)
                cart_item = CartItem.objects.filter(cart=cart.id)
                new_order = Order.objects.get(cart=cart)
            except:
                return HttpResponseRedirect("/shop/cartCheckout")

            if request.method == "POST":
                payment_type = request.POST.get("payment")

                if payment_type == "paytm":
                    # After payment, request paytm to transfer amount to our account done by customer
                    params_dict = {
                        'MID':settings.MERCHANT_ID,
                        'ORDER_ID':new_order.order_id,
                        'TXN_AMOUNT':str(cart.total_price),
                        'CUST_ID':user.email,
                        'INDUSTRY_TYPE_ID':'Retail',
                        'WEBSITE':settings.WEBSITE,
                        'CHANNEL_ID':'WEB',
                        'CALLBACK_URL':'http://127.0.0.1:8000/shop/paymentHandle/',
                        'MERC_UNQ_REF':str(user.id),
                    }
                    params_dict['CHECKSUMHASH'] = Checksum.generate_checksum(params_dict, settings.MERCHANT_KEY)
                    return render(request, 'shopping/paytm.html', {'params_dict':params_dict})

                elif payment_type == "credits":
                    now = datetime.now()
                    dt_string = now.strftime("%A, %B %d, %Y %I:%M %p")

                    params_dict = {
                        'credits':user.profile.credit,
                        'user':str(user.id),
                        'cart':cart,
                        'cart_item':cart_item,
                        'new_order':new_order,
                        'total_price':cart.total_price,
                        'txn_date':dt_string,
                        'payment':True,
                        'process':'cart',
                        }     
                    return render(request, "shopping/credits.html", {'params_dict':params_dict})

                else:
                    now = datetime.now()
                    dt_string = now.strftime("%A, %B %d, %Y %I:%M %p")

                    params_dict = {
                        'credits':user.profile.credit,
                        'user':str(user.id),
                        'cart':cart,
                        'cart_item':cart_item,
                        'new_order':new_order,
                        'total_price':cart.total_price,
                        'txn_date':dt_string,
                        'cod':True,
                        'process':'cart',
                        }     
                    return render(request, "shopping/cod.html", {'params_dict':params_dict})
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, "shopping/payment_method.html")

def codProcess(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i]=form[i]

    if response_dict['process'] == "buy":
        user = User.objects.get(id=response_dict['user'])
        buy = Buy.objects.get(user=user)
        buy_item = BuyItem.objects.get(buy=buy)
        new_order = Order.objects.get(buy=buy)

        if response_dict['cod']:
            try:
                product = Product.objects.get(product_name=buy_item.product)
                product.count_sold = product.count_sold + buy_item.quantity
                product.save()
            except Product.DoesNotExist:
                pass

            new_order.status = "Finished"
            new_order.save()
            print("Order Successful")
        
        else:
            new_order.delete()
            print("Order Unsuccessful")
        return render(request, 'shopping/cod_status.html', {'response':response_dict, 'credits_debited':buy.total_price, 'buy_thanks':True})

    else:
        user = User.objects.get(id=response_dict['user'])
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.filter(cart=cart)
        new_order = Order.objects.get(cart=cart)

        if response_dict['cod']:
            for cartitem in cart_item:
                try:
                    product = Product.objects.filter(product_name=cartitem.product)
                    for productitem in product:
                        productitem.count_sold = productitem.count_sold + cartitem.quantity
                        productitem.save()
                except Product.DoesNotExist:
                    pass

            new_order.status = "Finished"
            new_order.save()
            print("Order Successful")
        
        else:
            new_order.delete()
            print("Order Unsuccessful")
        return render(request, 'shopping/cod_status.html', {'response':response_dict, 'credits_debited':cart.total_price})
    return render(request, 'shopping/cod_status.html')

def creditProcess(request):
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i]=form[i]
    
    if response_dict['process'] == "buy":
        user = User.objects.get(id=response_dict['user'])
        buy = Buy.objects.get(user=user)
        buy_item = BuyItem.objects.get(buy=buy)
        new_order = Order.objects.get(buy=buy)

        if response_dict['payment']:
            new_total = 0.0
            # if don't have enough credits
            if float(user.profile.credit) < float(buy.total_price):
                new_total = float(buy.total_price) - float(user.profile.credit)
                buy.total_price = new_total
                buy.save()
                user.profile.credit = 0.0
                user.save()
                request.session['total_credits'] = user.profile.credit
                params_dict = {
                    'MID':settings.MERCHANT_ID,
                    'ORDER_ID':new_order.order_id,
                    'TXN_AMOUNT':str(buy.total_price),
                    'CUST_ID':user.email,
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE':settings.WEBSITE,
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':'http://127.0.0.1:8000/shop/paymentHandleBuy/',
                    'MERC_UNQ_REF':str(user.id),
                }
                params_dict['CHECKSUMHASH'] = Checksum.generate_checksum(params_dict, settings.MERCHANT_KEY)
                return render(request, 'shopping/paytm.html', {'params_dict':params_dict})
            else:
                # if have credits
                new_total = float(user.profile.credit) - float(buy.total_price)
                user.profile.credit = new_total
                user.save()
                request.session['total_credits'] = user.profile.credit

            try:
                product = Product.objects.get(product_name=buy_item.product)
                product.count_sold = product.count_sold + buy_item.quantity
                product.save()
            except Product.DoesNotExist:
                pass

            new_order.status = "Finished"
            new_order.is_amount_paid = True
            new_order.save()
            print("Order Successful")
        
        else:
            new_order.delete()
            print("Order Unsuccessful")
        return render(request, 'shopping/credit_status.html', {'response':response_dict, 'credits_debited':buy.total_price, 'buy_thanks':True})

    else:
        user = User.objects.get(id=response_dict['user'])
        cart = Cart.objects.get(user=user)
        cart_item = CartItem.objects.filter(cart=cart)
        new_order = Order.objects.get(cart=cart)

        if response_dict['payment']:
            new_total = 0.0
            # if don't have enough credits
            if float(user.profile.credit) < float(cart.total_price):
                new_total = float(cart.total_price) - float(user.profile.credit)
                cart.total_price = new_total
                cart.save()
                user.profile.credit = 0.0
                user.save()
                request.session['total_credits'] = user.profile.credit
                params_dict = {
                    'MID':settings.MERCHANT_ID,
                    'ORDER_ID':new_order.order_id,
                    'TXN_AMOUNT':str(cart.total_price),
                    'CUST_ID':user.email,
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE':settings.WEBSITE,
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':'http://127.0.0.1:8000/shop/paymentHandle/',
                    'MERC_UNQ_REF':str(user.id),
                }
                params_dict['CHECKSUMHASH'] = Checksum.generate_checksum(params_dict, settings.MERCHANT_KEY)
                return render(request, 'shopping/paytm.html', {'params_dict':params_dict})
            else:
                # if have credits
                new_total = float(user.profile.credit) - float(cart.total_price)
                user.profile.credit = new_total
                user.save()
                request.session['total_credits'] = user.profile.credit

            for cartitem in cart_item:
                try:
                    product = Product.objects.filter(product_name=cartitem.product)
                    for productitem in product:
                        productitem.count_sold = productitem.count_sold + cartitem.quantity
                        productitem.save()
                except Product.DoesNotExist:
                    pass

            new_order.status = "Finished"
            new_order.is_amount_paid = True
            new_order.save()
            print("Order Successful")
        
        else:
            new_order.delete()
            print("Order Unsuccessful")
        return render(request, 'shopping/credit_status.html', {'response':response_dict, 'credits_debited':cart.total_price})
    return render(request, 'shopping/credit_status.html')

@csrf_exempt
def paymentHandle(request):
    # PayTM will send us the post request here
    
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i]=form[i]
        if i == "CHECKSUMHASH":
            checksum = form[i]
    
    verify = Checksum.verify_checksum(response_dict, settings.MERCHANT_KEY, checksum)
    cart = Cart.objects.get(user=response_dict['MERC_UNQ_REF'])
    cartitems = CartItem.objects.filter(cart=cart)
    new_order = Order.objects.get(cart=cart)

    if verify:
        if response_dict['RESPCODE'] == '01':
            for cartitem in cartitems:
                try:
                    product = Product.objects.filter(product_name=cartitem.product)
                    for productitem in product:
                        productitem.count_sold = productitem.count_sold + cartitem.quantity
                        productitem.save()
                except Product.DoesNotExist:
                    pass

            curr_date = datetime.strptime(response_dict['TXNDATE'], "%Y-%m-%d %H:%M:%S.%f")
            new_date = curr_date.strftime("%A, %B %d, %Y %I:%M %p")
            response_dict['TXNDATE'] = new_date
            new_order.status = "Finished"
            new_order.is_amount_paid = True
            new_order.save()
            print("Order Successful")
        else:
            new_order.delete()
            print("Order Unsuccessful Because" + response_dict['RESPMSG'])
    else:
        new_order.delete()
        print("Order Unsuccessful Because" + response_dict['RESPMSG'])
    return render(request, 'shopping/paytm_status.html', {'response':response_dict})

@csrf_exempt
def paymentHandleBuy(request):
    # PayTM will send us the post request here
    
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i]=form[i]
        if i == "CHECKSUMHASH":
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, settings.MERCHANT_KEY, checksum)
    buy = Buy.objects.get(user=response_dict['MERC_UNQ_REF'])
    buyitem = BuyItem.objects.get(buy=buy)
    new_order = Order.objects.get(buy=buy)

    if verify:
        if response_dict['RESPCODE'] == '01':
            try:
                product = Product.objects.get(product_name=buyitem.product)
                product.count_sold = product.count_sold + buyitem.quantity
                product.save()
            except Product.DoesNotExist:
                pass
            
            curr_date = datetime.strptime(response_dict['TXNDATE'], "%Y-%m-%d %H:%M:%S.%f")
            new_date = curr_date.strftime("%A, %B %d, %Y %I:%M %p")
            response_dict['TXNDATE'] = new_date
            new_order.status = "Finished"
            new_order.is_amount_paid = True
            new_order.save()
            print("Order Successful")
        else:
            new_order.delete()
            print("Order Unsuccessful Because" + response_dict['RESPMSG'])
    else:
        new_order.delete()
        print("Order Unsuccessful Because" + response_dict['RESPMSG'])
    return render(request, 'shopping/paytm_status.html', {'response':response_dict, 'buy_thanks':True})

def orderDetails(request):
    if request.user.is_authenticated:
        request.session['total_credits'] = float(request.user.profile.credit)
        if request.user.profile.is_verified == "VF" and request.user.profile.is_email_verified == "VF":
            user = request.user
            new_order = Order.objects.filter(user=user).order_by('-id')
            if new_order.exists():
                page = request.GET.get('page', 1)
                paginator = Paginator(new_order, 5)
                try:
                    records = paginator.page(page)
                except PageNotAnInteger:
                    records = paginator.page(1)
                except EmptyPage:
                    records = paginator.page(paginator.num_pages)
                params = {'order':new_order, 'records':records}
            else:
                params = {'empty':True}

        else:
            return HttpResponseRedirect("/home/notVerified")
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, 'shopping/order_details.html', params)

def cartView(request):
    if request.user.is_authenticated:
        request.session['total_credits'] = float(request.user.profile.credit)
        if request.user.profile.is_verified == "VF" and request.user.profile.is_email_verified == "VF":
            try:
                user = request.user
                cart = Cart.objects.get(user=user)
                cart_id = cart.id
            except:
                cart_id = None

            if cart_id:
                cart = Cart.objects.get(id=cart_id)
                new_total = 0.00
                for item in cart.cartitem_set.all():
                    line_total = float(item.product.price) * item.quantity
                    new_total = new_total + line_total
                
                cart.total_price = new_total
                cart.save()

                params = {"cart":cart, 'cart_count':cart.cartitem_set.count()}
            else:
                params = {'empty':True}
        else:
            return HttpResponseRedirect("/home/notVerified")
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, "shopping/cartView.html", params)

def remove_from_cart(request, id):
    try:
        user = request.user
        cart = Cart.objects.get(user=user)
    except:
        return HttpResponseRedirect(reverse("cartView"))
    
    cartitem = CartItem.objects.get(id=id)
    cartitem.delete()
    messages.error(request, "Item removed from your cart.")
    request.session['items_total'] = cart.cartitem_set.count()

    return HttpResponseRedirect(reverse("cartView"))
        
def add_to_cart(request, id):
    if request.user.is_authenticated:
        request.session['total_credits'] = float(request.user.profile.credit)
        if request.user.profile.is_verified == "VF" and request.user.profile.is_email_verified == "VF":
            try:
                user = request.user
                cart = Cart.objects.get(user=user)
            except Cart.DoesNotExist:
                cart = Cart()
                cart.user = request.user
                cart.save()
            
            cart = Cart.objects.get(id=cart.id)

            try:
                product = Product.objects.get(id=id)
            except Product.DoesNotExist:
                pass
            except: 
                pass

            if request.method == "POST":
                try:
                    qty = int(request.POST['qty'])
                    cart_item = CartItem.objects.get(cart=cart, product=product)
                    cart_item.quantity += qty
                    cart_item.save()
                except CartItem.DoesNotExist:
                    qty = request.POST['qty']
                    cart_item = CartItem.objects.create(cart=cart, product=product)
                    cart_item.quantity = qty
                    cart_item.save()
                request.session['items_total'] = cart.cartitem_set.count()
                messages.success(request, "Item added to your cart.")
                return HttpResponseRedirect(f"/shop/productView/{id}")
        else:
            return HttpResponseRedirect("/home/notVerified")
    else:
        return HttpResponseRedirect("/home/cannot_access")

    return HttpResponseRedirect(reverse("cartView"))

def buy_now(request, id):
    if request.user.is_authenticated:
        request.session['total_credits'] = float(request.user.profile.credit)
        if request.user.profile.is_verified == "VF" and request.user.profile.is_email_verified == "VF":
            buy = Buy.objects.filter(user=request.user)
            buy.delete()
            try:
                user = request.user
                buy = Buy.objects.get(user=user)
            except Buy.DoesNotExist:
                buy = Buy()
                buy.user = request.user
                buy.save()
            
            buy = Buy.objects.get(id=buy.id)

            try:
                product = Product.objects.get(id=id)
            except Product.DoesNotExist:
                pass
            except: 
                pass

            buy.total_price = product.price
            buy.save()

            try:
                buy_item = BuyItem.objects.get(buy=buy, product=product)
                buy_item.save()
            except BuyItem.DoesNotExist:
                buy_item = BuyItem.objects.create(buy=buy, product=product)
                buy_item.save()
            return render(request, "shopping/new_checkout.html", {'buy':buy, 'buy_item':buy_item, 'thanks':True})
        else:
            return HttpResponseRedirect("/home/notVerified")
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, "shopping/new_checkout.html")

def cart_item_count(request):
    try:
        user = request.user
        cart = Cart.objects.get(user=user)
        new_order = Order.objects.get(cart=cart)
        if new_order.status == "Finished":
            del request.session['items_total']
            cart.delete()
            request.session['items_total'] = 0 
            return HttpResponseRedirect(reverse("shoppingHome"))
    except Order.DoesNotExist:
        return HttpResponseRedirect(reverse("shoppingHome"))
    return HttpResponseRedirect(reverse("shoppingHome"))

def buy_item_count(request):
    try:
        user = request.user
        buy = Buy.objects.get(user=user)
        new_order = Order.objects.get(buy=buy)
        if new_order.status == "Finished":
            buy.delete()
            return HttpResponseRedirect(reverse("shoppingHome"))
    except Order.DoesNotExist:
        return HttpResponseRedirect(reverse("shoppingHome"))
    return HttpResponseRedirect(reverse("shoppingHome"))

def review(request, url):
    if request.user.is_authenticated:
        request.session['total_credits'] = float(request.user.profile.credit)
        product = Product.objects.get(slug=url)
        comments = Comment.objects.filter(product=product, user=request.user)
        if comments.exists():
            params = {'product': product, 'comments':comments[0], 'status':True}
            if request.method == "POST":
                review = Comment.objects.get(product=product, user=request.user)
                review.subject = request.POST.get("subject")
                review.comment = request.POST.get("comment")
                review.rating = request.POST.get("rating")
                review.save()
                messages.success(request, "Your review has been sent. Thank You for your interest.")
                return HttpResponseRedirect(f"/shop/review/{url}")     
        else:
            params = {'product': product, 'status':False}
            if request.method == "POST":
                subject = request.POST.get("subject")
                review = request.POST.get("comment")
                rating = request.POST.get("rating")
                product = Product.objects.get(slug=url)
                user = request.user

                comment = Comment(product=product, user=user, subject=subject, comment=review, rating=rating)
                comment.save()
                messages.success(request, "Your review has been sent. Thank You for your interest.")
                return HttpResponseRedirect(f"/shop/review/{url}")
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, "shopping/review.html", params)

def pincodeCheck(request):
    if request.method == "POST":
        try:
            pincode = request.POST.get("pincode")
            if len(pincode) < 1:
                return HttpResponse('{"status":"not_success", "message":"Required field. Cannot be empty. Provide 6 digit pincode"}')
            elif not PINCODE_REGEX.match(pincode):
                return HttpResponse('{"status":"not_success", "message":"Please provide 6 digit pincode"}')
            else:
                r = requests.get(f"https://api.postalpincode.in/pincode/{pincode}")
                j = r.json()

                now = datetime.now()
                saved_datetime = now + timedelta(days=7)
                dt_string = saved_datetime.strftime("%A, %B %d")

                if j[0]['Status'] != "Error":
                    pincode_list = []
                    for i in j[0]['PostOffice']:
                        if i['DeliveryStatus'] == "Delivery":
                            pincode_list.append({"name":i['Name'], "delivery":i['DeliveryStatus'], "district":i['District'], "state":i['State']})
                            res = json.dumps({"status": "success", "message":"Delivery Available", "date":dt_string, "pincode":pincode_list}, default=str)
                    return HttpResponse(res)
                else:
                    return HttpResponse('{"status": "not_success", "message":"Error! Postal Code invalid. Please enter a valid postal code."}')
        except Exception as e:
            return HttpResponse('{"status": "not_success", "message":"Error! Please try after some time."}')
    return render(request, "shopping/product_view.html")



