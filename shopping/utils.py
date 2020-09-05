import string
import random

from shopping.models import Order

def orderid_generator(size=15, chars=string.ascii_uppercase + string.digits):
    order_id = "".join(random.choice(chars) for x in range(size))
    try:
        order = Order.objects.get(order_id=order_id)
        orderid_generator()
    except Order.DoesNotExist:
        return order_id

def refid_generator(size=10, chars=string.ascii_uppercase + string.digits):
    ref_id = "".join(random.choice(chars) for x in range(size))
    try:
        order = Order.objects.get(reference_id=ref_id)
        refid_generator()
    except Order.DoesNotExist:
        return ref_id