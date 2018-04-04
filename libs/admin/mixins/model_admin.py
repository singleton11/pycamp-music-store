import json
from functools import partial
from urllib.parse import parse_qs

from django import forms
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory
from django.utils.html import format_html
from django.utils.safestring import mark_safe

__all__ = (
    'ForbidDeleteAdd',
    'FkAdminLink',
    'AllFieldsReadOnly',
)


def _parse_url_params_changelist_filter(request):
    """Method to extract field names and object ids from URL.
    Used in InitialValuesMixin and CustomBreadcrumbsMixin.

    Example:
    admin/notes/note/add/?_changelist_filters=module__module_ptr__exact%3D7
    """

    query_string = parse_qs(request.META['QUERY_STRING'])
    params_string = query_string.get('_changelist_filters')

    if not params_string:
        return {}

    # In case if there are more than 1 filter param
    params = parse_qs(params_string[0])

    parsed_fields = {}
    for field_name, object_id in params.items():
        # field_name = 'module__module_ptr__exact' -> 'module'
        field_name = field_name.split('__')[0]
        parsed_fields.update({field_name: object_id[0]})

    return parsed_fields


class ForbidDeleteAdd(object):
    """Added forbid permission for objects.

    The mixin redefining two methods of ``ModelAdmin`` and both these methods
    will return false, do not allow adding and deleting objects.

    """

    def delete_model(self, request, obj):
        """Does nothing on delete"""
        return

    def get_actions(self, request):
        """Disables "delete_selected" action
        """
        actions = super().get_actions(request)

        if 'delete_selected' in actions:
            del actions['delete_selected']

        return actions

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class FkAdminLink(object):
    """Link to object in admin.

    Example:

        class Book(models.Model):
            author = models.ForeignKey('user')
            content = models.TextField()


        class BookAdmin(models.ModelAdmin):
            readonly_fields = ('_author',)

            def _author(self, obj):
                return self._admin_url(obj.author)

            # or with title

            def _author(self, obj):
                return self._admin_url(
                    obj.author,
                    obj.author.last_name + obj.author.first_name[0]
                )

    """

    def _get_admin_url(self, obj):
        admin_url_str = 'admin:{}_{}_change'.format(
            obj._meta.app_label,
            obj._meta.object_name.lower()
        )
        return reverse(admin_url_str, args=[obj.pk])

    def _admin_url(self, obj, title=None):
        admin_url = self._get_admin_url(obj)
        return format_html(
            "<a href='{0}' target='_blank'>{1}</a>",
            admin_url, title or str(obj))


class AllFieldsReadOnly(object):
    """Make all field read only.

    Simple mixin if you want to make all fields readonly without specifying
    fields attribute.

    """

    def get_readonly_fields(self, request, obj=None):
        if self.fields:
            return self.fields

        # took this django sources
        if self.exclude is None:
            exclude = []
        else:
            exclude = list(self.exclude)

        if (self.exclude is None and hasattr(self.form, '_meta') and
                self.form._meta.exclude):
            # Take the custom ModelForm's Meta.exclude into account only if the
            # ModelAdmin doesn't define its own.
            exclude.extend(self.form._meta.exclude)

        # if exclude is an empty list we pass None to be consistent with the
        # default on modelform_factory
        exclude = exclude or None

        defaults = {
            'form': self.form,
            'fields': forms.ALL_FIELDS,
            'exclude': exclude,
            'formfield_callback': partial(
                self.formfield_for_dbfield,
                request=request
            )
        }
        form = modelform_factory(self.model, **defaults)

        return list(form.base_fields)


class PrettyPrintMixin(object):
    """Mixin for pretty displaying readonly python objects in admin.

    May be used for pretty displaying complex objects, like dicts, lists.

    Provide one method - `pretty_print`
    """

    def pretty_print(self, obj):
        """Returns pretty jsoned representation of ``obj``"""
        return mark_safe(json.dumps(obj, indent=4)
                         .replace(' ', '&nbsp').replace('\n', '<br>'))


class InitialValuesAdminMixin(object):
    """Mixin class that adds initial values to Model Admin.

    This mixin works on account of Django changelist filters (in URL).

    For example, you selected specific `Module` on changelist for `Note` and
    clicked `Add Note` button. Following page will have URL:

        admin/notes/note/add/?_changelist_filters=module__module_ptr__exact%3D7

    After parsing this URL, this mixin extract following params:

        {'module__module_ptr__exact':'7'}

    And then mixin extracts field name from first words before '__'. If such
    field (in this case: 'module') exist in Model Admin form then it will be
    set to `Module` that have id=7.

    """

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Custom `formfield_for_foreignkey` method.

        This method sets initial values for fields that were found by
        `_parse_url_params_changelist_filter` method.

        """
        res = super().formfield_for_foreignkey(db_field, request, **kwargs)
        parsed_fields = _parse_url_params_changelist_filter(request)

        object_id = parsed_fields.get(db_field.name)
        if object_id and not res.initial:
            model = db_field.related_model
            try:
                res.initial = model.objects.filter(id=object_id).first()
            except ValueError:
                # In case if passed `object_id` didn't match format
                pass

        return res


class DisabledFieldsMixin(object):
    """Mixin class for Model Admin to disable specific ForeignKey fields.

    This mixin makes widget for specified ForeignKey fields as disabled
    in case if object already exists. It helps to prevent field modifying
    after object is created. For example, `Conference` and `Module` fields.

    This mixin works normally with default `Select` widget and with custom
    `AutocompleteWidget` (second looks more naturally).

    TODO: Doesn't work with `CustomFieldsModelAdminMixin` properly.
    For example: In `ListItemAdmin` this mixin should be higher in MRO
    than `CustomFieldsModelAdminMixin`

    Attributes:
        disabled_fields (tuple): tuple of field names to disable

    """
    disabled_fields = tuple()

    def get_form(self, request, obj=None, **kwargs):
        """Custom `get_form` method.

        Sets fields as disabled if object already exists.

        """
        form = super().get_form(request, obj, **kwargs)

        for field_name in self.disabled_fields:
            field = form.base_fields[field_name]
            field.disabled = bool(obj)

        return form
