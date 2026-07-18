class CouponException(Exception):
    pass


class CouponExpired(CouponException):
    pass


class CouponInactive(CouponException):
    pass


class CouponAlreadyUsed(CouponException):
    pass


class CouponUsageExceeded(CouponException):
    pass