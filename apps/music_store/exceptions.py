from django.core.exceptions import ValidationError


class ItemAlreadyBought(ValidationError):
    """ Error that raise when user try to buy already bought item"""

    def __init__(self):
        super().__init__("Already Bought")


class NotEnoughMoney(ValidationError):
    """ Error that raise when user not have enough money"""

    def __init__(self):
        super().__init__("Not enough money")


class PaymentNotFound(ValidationError):
    """ Error that raise when user not have payment method"""

    def __init__(self):
        super().__init__("Payment method not found")
