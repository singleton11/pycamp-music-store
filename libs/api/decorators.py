def push_notification(push_notification_classes=None):
    """
    Used to mark a method with push_notifications.
    """

    def decorator(func):
        func.push_notification_classes = push_notification_classes
        return func
    return decorator
