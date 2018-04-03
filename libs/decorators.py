from django.conf import settings

from celery import shared_task

from .utils import get_attr


def related_properties(**properties):
    """Returns decorator which added some properties to your class

    Examples:

        class Conference(Model):
            "Conference itself"
            ...

        class Module(Model):
            "Module related to Conference model"
            conference = ForeignKey('Conference')

        @related_properties(conference='module.conference')
        class Event(Model):
            module = ForeignKey('Module')

        event = Event(...)
        # this call
        print(event.conference)
        # is the same as
        print(event.module.conference)

    Args:
        properties (dict): property name -> property path

    Returns:
        class: decorated class with properties
    """
    def decorator(klass):

        def _property(property_path):
            """Property factory

            Args:
                property_path (str): path to property
            """
            def get_prop(self):
                return get_attr(self, property_path, default=None)

            return property(get_prop)

        for prop, prop_path in properties.items():
            assert not hasattr(klass, prop), (
                "Decorated class already has property '{0}'".format(prop)
            )
            setattr(klass, prop, _property(prop_path))

        return klass

    return decorator


def extended_shared_task(*decorator_args, **decorator_kwargs):
    """Decorator to avoid boilerplate with `shared_task` decorator.

    Allow avoid following code:

        if settings.USE_CELERY:
            some_task.delay(**kwargs)
        else:
            some_task(**kwargs)
    """
    def extended_shared_task_decorator(func):
        func = shared_task(func, *decorator_args, **decorator_kwargs)

        def _wrapped(*args, **kwargs):
            if settings.USE_CELERY:
                return func.delay(*args, **kwargs)
            return func(*args, **kwargs)

        return _wrapped

    return extended_shared_task_decorator
