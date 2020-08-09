from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from shopping.models import Product, Contact, Orders, OrdersUpdate, PaytmKey, Cart, CartItem, Order, Buy, BuyItem, BannerImage, YoutubeLink, Comment
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

paytm = PaytmKey.objects.values('merchant_id', 'merchant_key')
for item in paytm:
    merchant_id = item['merchant_id']
    merchant_key = item['merchant_key']
MERCHANT_KEY = merchant_key

# Create your views here.
def index(request):
    all_products = []
    latest_products = []
    trending_products = []

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

    product_category = Product.objects.values('category','id')
    categories = {item['category'] for item in product_category}
    for category in categories:
        prod = Product.objects.filter(category = category).order_by('category')
        n = len(prod)
        no_slides = n // 4 + ceil((n / 4) - (n // 4))
        all_products.append([prod, range(1, no_slides), no_slides])

    banner_image = BannerImage.objects.all()
    youtube_link = YoutubeLink.objects.all()[0]
    params = {'all_products':all_products, 'banner':banner_image, 'youtube':youtube_link, 'all_latest_products':latest_products, 'all_trending_products':trending_products}
    return render(request, 'shopping/index.html', params)

def contact(request):
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
        if request.user.profile.is_verified == "VF":
            if request.method == 'POST':
                orderid = request.POST.get("orderid", default="")
                
                try:
                    order = Order.objects.filter(order_id=orderid, user=request.user)
                    if len(order) > 0:
                        update = OrdersUpdate.objects.filter(order_id=orderid)
                        updates = []
                        for item in update:
                            updates.append({'text':item.update_description, 'time':item.timestamp})
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
    #Fetching product using id
    product = Product.objects.get(id = id)
    comments = Comment.objects.filter(product=product).order_by('id')

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
    if request.user.profile.is_verified == "VF":
        thanks = request.POST.get("buy_thanks")
        if thanks:
            try:
                user = request.user
                buy = Buy.objects.get(user=user)
                buy_item = BuyItem.objects.filter(buy=buy.id)
                
                items = []
                for item in buy_item:
                    items.append([item.product.product_name, item.quantity, item.product.slug])
            except:
                return HttpResponseRedirect(reverse("new_checkout"))
            
            if request.method == "POST":
                name = request.POST.get("name", default="")
                email = request.POST.get("email", default="")
                address1 = request.POST.get("address1", default="")
                address2 = request.POST.get("address2", default="")
                city = request.POST.get("city", default="")
                state = request.POST.get("state", default="")
                zip_code = request.POST.get("zip_code", default="")
                mobile_number = request.POST.get("mobile_number", default="")

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
                    new_order.save()
                except:
                    return HttpResponseRedirect(reverse("new_checkout"))

                orders_update = OrdersUpdate(order_id=new_order.order_id, update_description="Your order has been placed") 
                orders_update.save()

                # After payment, request paytm to transfer amount to our account done by customer
                params_dict = {
                    'MID':merchant_id,
                    'ORDER_ID':new_order.order_id,
                    'TXN_AMOUNT':str(buy.total_price),
                    'CUST_ID':email,
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE':'WEBSTAGING',
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':'http://127.0.0.1:8000/shop/paymentHandleBuy/',
                    'MERC_UNQ_REF':str(user.id),
                }
                params_dict['CHECKSUMHASH'] = Checksum.generate_checksum(params_dict, MERCHANT_KEY)
                return render(request, 'shopping/paytm.html', {'params_dict':params_dict})
            return render(request, "shopping/new_checkout.html", {'buy_item':buy_item, 'buy_total':buy.total_price})

        else:
            try:
                user = request.user
                cart = Cart.objects.get(user=user)
                cart_item = CartItem.objects.filter(cart=cart.id)
                items = []
                for item in cart_item:
                    items.append([item.product.product_name, item.quantity, item.product.slug])
            except:
                return HttpResponseRedirect(reverse("cartView"))

            if request.method == "POST":
                name = request.POST.get("name", default="")
                email = request.POST.get("email", default="")
                address1 = request.POST.get("address1", default="")
                address2 = request.POST.get("address2", default="")
                city = request.POST.get("city", default="")
                state = request.POST.get("state", default="")
                zip_code = request.POST.get("zip_code", default="")
                mobile_number = request.POST.get("mobile_number", default="")

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
                    new_order.save()
                except:
                    return HttpResponseRedirect(reverse("cartview"))

                orders_update = OrdersUpdate(order_id=new_order.order_id, update_description="Your order has been placed") 
                orders_update.save()
                
                # After payment, request paytm to transfer amount to our account done by customer
                params_dict = {
                    'MID':merchant_id,
                    'ORDER_ID':new_order.order_id,
                    'TXN_AMOUNT':str(cart.total_price),
                    'CUST_ID':email,
                    'INDUSTRY_TYPE_ID':'Retail',
                    'WEBSITE':'WEBSTAGING',
                    'CHANNEL_ID':'WEB',
                    'CALLBACK_URL':'http://127.0.0.1:8000/shop/paymentHandle/',
                    'MERC_UNQ_REF':str(user.id),
                }
                params_dict['CHECKSUMHASH'] = Checksum.generate_checksum(params_dict, MERCHANT_KEY)
                return render(request, 'shopping/paytm.html', {'params_dict':params_dict})
            return render(request, "shopping/new_checkout.html", {'cart_item':cart_item, 'cart_total':cart.total_price})
    else:
        return HttpResponseRedirect("/home/notVerified")
    return render(request, "shopping/new_checkout.html")

def checkout(request):
    if request.method == 'POST':
        items_json = request.POST.get("itemsjson", default="")
        name = request.POST.get("name", default="")
        email = request.POST.get("email", default="")
        address1 = request.POST.get("address1", default="")
        address2 = request.POST.get("address2", default="")
        city = request.POST.get("city", default="")
        state = request.POST.get("state", default="")
        zip_code = request.POST.get("zip_code", default="")
        mobile_number = request.POST.get("mobile_number", default="")
        total_price = request.POST.get("total_price", default="")
        orders = Orders(items_json=items_json, name=name, email=email, address1=address1, address2=address2, city=city, state=state, zip_code=zip_code, mobile_number=mobile_number, total_price=total_price)
        orders.save()

        orders_update = OrdersUpdate(order_id=orders.order_id, update_description="Your order has been placed") 
        orders_update.save()
        
        thanks = True
        order_id = orders.order_id

        # After payment, request paytm to transfer amount to our account done by customer
        params_dict = {
            'MID':merchant_id,
            'ORDER_ID':str(orders.order_id),
            'TXN_AMOUNT':str(total_price),
            'CUST_ID':email,
            'INDUSTRY_TYPE_ID':'Retail',
            'WEBSITE':'WEBSTAGING',
            'CHANNEL_ID':'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/shop/paymentHandle/',
        }
        params_dict['CHECKSUMHASH'] = Checksum.generate_checksum(params_dict, MERCHANT_KEY)
        return render(request, 'shopping/paytm.html', {'params_dict':params_dict})
    return render(request, 'shopping/checkout.html')

@csrf_exempt
def paymentHandle(request):
    # PayTM will send us the post request here
    
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i]=form[i]
        if i == "CHECKSUMHASH":
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    cart = Cart.objects.get(user=form['MERC_UNQ_REF'])
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
            new_order.status = "Finished"
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

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    buy = Buy.objects.get(user=form['MERC_UNQ_REF'])
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

            new_order.status = "Finished"
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
        if request.user.profile.is_verified == "VF":
            user = request.user
            new_order = Order.objects.filter(user=user).order_by('-id')
            if new_order.exists():
                params = {'order':new_order}
            else:
                params = {'empty':True}

        else:
            return HttpResponseRedirect("/home/notVerified")
    else:
        return HttpResponseRedirect("/home/cannot_access")
    return render(request, 'shopping/order_details.html', params)

def cartView(request):
    if request.user.is_authenticated:
        if request.user.profile.is_verified == "VF":
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
        if request.user.profile.is_verified == "VF":
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
        if request.user.profile.is_verified == "VF":
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
        return HttpResponseRedirect(reverse("cartView"))
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
        return HttpResponseRedirect(reverse("cartView"))
    return HttpResponseRedirect(reverse("shoppingHome"))

def review(request, url):
    if request.user.is_authenticated:
        product = Product.objects.get(slug=url)
        comments = Comment.objects.filter(product=product)
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
    return render(request, "shopping/review.html", params)



