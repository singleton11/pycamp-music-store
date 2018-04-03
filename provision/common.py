def message(text):
    """Format message
    Args:
        text (str): textual message to format
    """
    length = len(text) if len(text) > 76 else 76

    msg = "\n"
    msg += "o" * (length + 4) + "\n"
    msg += "o {:76s} o\n".format(text)
    msg += "o" * (length + 4) + "\n"
    return msg
