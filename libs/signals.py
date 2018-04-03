__all__ = (
    'M2MChangedSignalHandler',
)


class M2MChangedSignalHandler(object):
    """This class can be used as M2M signal handlers

    All M2M signals in Django are handled by one handler, which gets ``action``
    attribute. ``action`` contains signal type (post_add, post_remove,
    post_clear, etc.) More about m2m signals you can find in Django docs.

    This class has one method - ``handle`` which has the same signature as
    m2m-signal's handler.

    To add processing of specific m2m signal you need to implement
    appropriate method for specific action.

    Examples:

        # implement handler

        class MyM2MHandler(M2MChangedSignalHandler):
            def post_add(self):
                # do something

            def post_remove(self):
                # do something

        # register handler
        # as soon as signal must be function (not class method) we have to
        # register this handler in this way

        @receiver(m2m_changed, sender=AppUser.groups.through)
        def signal_m2m_changed_auth_group(**kwargs):
            MyM2MHandler(**kwargs).handle()
    """

    def __init__(
            self, sender, instance, action, reverse, model, pk_set, **kwargs):
        self.sender = sender
        self.instance = instance
        self.action = action
        self.reverse = reverse
        self.model = model
        self.pk_set = pk_set or ()
        self.kwargs = kwargs

    def handle(self):
        handler = getattr(self, self.action, None)
        if not handler:
            return
        handler()

    def pre_add(self):
        pass

    def post_add(self):
        pass

    def pre_remove(self):
        pass

    def post_remove(self):
        pass

    def pre_clear(self):
        pass

    def post_clear(self, sender, instance, reverse, model, pk_set, **kwargs):
        pass
