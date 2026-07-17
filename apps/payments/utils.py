from decimal import Decimal


def amount_to_paise(amount: Decimal) -> int:
    """
    Convert INR to paise.
    Example:
        499.99 -> 49999
    """
    return int(amount * 100)


def paise_to_amount(paise: int) -> Decimal:
    """
    Convert paise to INR.
    Example:
        49999 -> 499.99
    """
    return Decimal(paise) / Decimal("100")