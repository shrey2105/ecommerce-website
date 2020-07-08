import string
import random

from home.models import PhoneOtp

def otp_key_generator(user_mobile, size=6, chars=string.ascii_uppercase + string.digits):
    otp = "".join(random.choice(chars) for x in range(size))
    if user_mobile:
        try:
            order = PhoneOtp.objects.get(otp=otp)
            otp_key_generator()
        except PhoneOtp.DoesNotExist:
            return otp
    else:
        return False