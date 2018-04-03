from functools import partial

import inflection


def hide_except_last(value, num=4):
    """Used to hide everything but last num letters of the string value
    Attributes:
        value (str): String to obfuscate
        num (int): How many latters to keep visible
    Returns:
        obfuscated string where first letters are hidden with *
    """
    return '*'*(len(value)-num)+value[-num:]


def convert(item, method):
    """Will apply conversion method to item
    Attributes:
        item (str | list): what to convert
        method (func): reference to conversion function
    Returns:
        converted item
    """
    if isinstance(item, str):
        return method(item)
    return list(map(method, item))


# partials
titleize = partial(convert, method=inflection.titleize)
humanize = partial(convert, method=inflection.humanize)

__all__ = (
    'titleize',
    'humanize',
)
