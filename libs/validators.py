from django.core.exceptions import ValidationError
from .utils import calculate_age


def less_than_18(value):
    if calculate_age(value) < 18:
        raise ValidationError("You're too young to use this application!")
