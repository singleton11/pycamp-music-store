from urllib.parse import urlencode

from django.core.urlresolvers import reverse
from django.forms.models import _get_foreign_key as get_foreign_key
from django.http import HttpResponseRedirect

from django_object_actions import DjangoObjectActions


class RelatedObjectActionsMixin(DjangoObjectActions):
    """Related object actions mixin.

    This mixin is used for adding link buttons to changelist for related models
    to the parent admin class.

    We have two admins for Conference and Banner (has ForeignKey to Conference)
    models, Conference admin url is:

        - /admin/conferences/conference/123456/

    The mixin adds `Banner` button to `Conference` admin that redirects
    user to this url:

        - /admin/conferences/banner/?conference__id__exact=123456

    For use the mixin need to add to Admin class the mixin and
    ``related_models`` attribute:

        class ConferenceAdmin(RelatedObjectActionsMixin, admin.ModelAdmin):
            # ...
            related_models = (Banner,)

    Also `related_models` objects can be a tuple instead of just model. In that
    case mixin will search for specific field in model (instead of finding it
    automatically). For example, `Banner` has `conference` ForeignKey field:

        related_models = ((Banner, 'conference'),)

    Buttons added using DjangoObjectActions. See method ``change_actions``.

    Note: `related_models` is a required attribute, but if you want to skip it,
    then set `related_models = False`.

    Attributes:
        related_models (tuple): tuple of related model definitions.

    """
    related_models = []
    extra_change_actions = []

    @property
    def change_actions(self):
        """Some magic to add links to related admins.

        This should be property containing list of ALL change actions avalable
        for the model. But here we create it dynamically.

        Logic:
            * take all related models
            * create **new** method of `self` that redirects to proper admin
            * return list of strings

        This method is being called few times, so there is a check that
        tools does not registered twice.

        """
        change_actions = super().change_actions.copy()

        for related_model_definition in self.related_models:
            # If model definition is a tuple/list then there is a fk_name
            if type(related_model_definition) in (tuple, list):
                related_model, fk_name = related_model_definition
            # Otherwise, fk_field will be obtained automatically
            else:
                related_model, fk_name = related_model_definition, None

            related_model_name = related_model._meta.verbose_name_plural

            method_name = 'tool_redirect_to_{}'.format(
                related_model._meta.model_name
            )
            if method_name in change_actions:
                continue

            # Get `changelist` URL for model
            changelist_url = 'admin:{0}_{1}_changelist'.format(
                related_model._meta.app_label,
                related_model._meta.model_name,
            )

            # Get `related_model` ForeignKey field to `self.model`
            fk_field = get_foreign_key(
                parent_model=self.model,
                model=related_model,
                fk_name=fk_name
            )

            def view_template(
                self, request, obj, fk_field=fk_field,
                changelist_url=changelist_url
            ):
                """Template of object action that will be added to this admin.

                Simply redirects user to `filtered_url`.

                """
                filter_arg = urlencode(
                    fk_field.get_forward_related_filter(obj)
                )
                filtered_url = (
                    '{changelist_url}?{filter_arg}'
                    .format(
                        changelist_url=reverse(changelist_url),
                        filter_arg=filter_arg.replace('=', '__exact=')
                    )
                )
                return HttpResponseRedirect(filtered_url)

            view_template.label = related_model_name
            view_template.short_description = related_model_name

            method_name = 'tool_redirect_to_{}'.format(
                related_model._meta.model_name
            )
            setattr(self.__class__, method_name, view_template)
            change_actions.append(method_name)

        return list(change_actions) + list(self.extra_change_actions)
