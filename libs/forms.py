from django import forms
from django.utils.translation import ugettext_lazy as _

from funcy import walk


class CleanNotEmptyFieldsForm(object):
    """By default `full_clean` method for model's form successively runs
    `_clean_fields`, `_clean_form` and `_post_clean`. And all ValidationErrors
    which were raised inside them are placed in try-except block and
    collected in form's `self.errors` list.

    In model `clean` method sometimes we  need to retrieve values for
    FK-fields.
    In this case if user set this filed empty in admin form, then
    attempt to get value for this filed from db raise
    `RelatedObjectDoesNotExist` error.

    That's why we shouldn't call `clean` for model instance.

    We get this problem for new instances with empty FK-field.

    User should add iterable `post_clean_free_fields` attribute into class
    and place into it fields which shouldn't have errors before `_post_clean`
    would called
    """
    def __init__(self, *args, **kwargs):
        assert isinstance(self, forms.BaseModelForm), _(
            'Form class should be instance of `BaseModelForm`'
        )

        assert hasattr(self, 'post_clean_free_fields'), _(
            'You should add model fields into `post_clean_free_fields` attr'
        )

        super().__init__(*args, **kwargs)

    def _post_clean(self):
        if any(walk(self.errors.__contains__, self.post_clean_free_fields)):
            return

        super()._post_clean()
