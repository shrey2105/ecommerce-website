from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from shopping.models import Product, Contact, Orders, OrdersUpdate, PaytmKey
from django.contrib import messages
from math import ceil
import json
from django.views.decorators.csrf import csrf_exempt
from PayTM import Checksum

paytm = PaytmKey.objects.values('merchant_id', 'merchant_key')
for item in paytm:
    merchant_id = item['merchant_id']
    merchant_key = item['merchant_key']
MERCHANT_KEY = merchant_key

# Create your views here.
def index(request):
    all_products = []
    product_category = Product.objects.values('category','id')
    categories = {item['category'] for item in product_category}
    for category in categories:
        prod = Product.objects.filter(category = category)
        n = len(prod)
        no_slides = n // 4 + ceil((n / 4) - (n // 4))
        all_products.append([prod, range(1, no_slides), no_slides])
    params = {'all_products':all_products}
    return render(request, 'shopping/index.html', params)

def about(request):
    return render(request, 'shopping/about.html')

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
            order = Orders.objects.filter(order_id=orderid, email=email)
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
    product = Product.objects.filter(id = id)
    params = {'product':product[0]}
    return render(request, 'shopping/product_view.html', params)

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
        # params = {'thanks':thanks, 'order_id':order_id}
        # return render(request, 'shopping/empty_cart.html', params)
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

def emptyCart(request):
    return render(request, 'shopping/empty_cart.html')

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
    print(verify)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print("Order Successful")
        else:
            print("Order Unsuccessful Because" + response_dict['RESPMSG'])
    else: 
        print("Order Unsuccessful Because" + response_dict['RESPMSG'])
    return render(request, 'shopping/paytm_status.html', {'response':response_dict})

def orderDetails(request):
    return render(request, 'shopping/order_details.html')


