import razorpay

from django.conf import settings


class RazorpayGateway:

    @staticmethod
    def client():

        return razorpay.Client(
            auth=(
                settings.RAZORPAY_KEY_ID,
                settings.RAZORPAY_KEY_SECRET,
            )
        )