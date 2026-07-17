from .models import PaymentProvider, PaymentStatus


SUPPORTED_PAYMENT_PROVIDERS = [
    PaymentProvider.COD,
    PaymentProvider.RAZORPAY,
]


SUCCESS_PAYMENT_STATUSES = [
    PaymentStatus.SUCCESS,
]


FAILED_PAYMENT_STATUSES = [
    PaymentStatus.FAILED,
]