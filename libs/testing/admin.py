from django.contrib.admin.sites import AdminSite
from django.core.exceptions import FieldError
from django.core.urlresolvers import reverse
from django.test import RequestFactory, tag

from apps.users.factories import AdminUserFactory

__all__ = (
    'TestAdminFieldsMixin',
    'TestRelatedObjectActionsMixin',
    'TestInitialValuesAdminMixin',
    'TestDisabledFieldsMixin',
)


@tag('admin')
class AdminTestShortcuts(object):
    """Class with shortcuts for testing Model Admin."""
    factory = None
    model_admin = None
    _factory = RequestFactory()

    def setUp(self):
        super().setUp()
        assert self.factory, '`factory` attribute is not specified.'
        assert self.model_admin, '`model_admin` attribute is not specified.'

    def get_model(self):
        """Shortcut to get model using factory."""
        return self.factory._meta.model

    def get_admin_instance(self):
        """Returns instance of admin class"""
        return self.model_admin(self.get_model(), AdminSite())

    def get_add_view_url(self):
        """Returns URL to object's add view."""
        url_name = (
            'admin:{meta.app_label}_{meta.model_name}_add'
            .format(meta=self.get_model()._meta)
        )
        return reverse(url_name)

    def get_change_view_url(self, obj):
        """Returns URL to object's change view."""
        url_name = (
            'admin:{meta.app_label}_{meta.model_name}_change'
            .format(meta=self.get_model()._meta)
        )
        return reverse(url_name, args=(obj.pk,))

    def get_changelist_view_url(self):
        """Returns URL to object's changelist view."""
        url_name = (
            'admin:{meta.app_label}_{meta.model_name}_changelist'
            .format(meta=self.get_model()._meta)
        )
        return reverse(url_name)

    def get_delete_view_url(self, obj):
        """Returns URL to object's delete view."""
        url_name = (
            'admin:{meta.app_label}_{meta.model_name}_delete'
            .format(meta=self.get_model()._meta)
        )
        return reverse(url_name, args=(obj.pk,))


class TestAdminFieldsMixin(AdminTestShortcuts):
    """Mixin for tests of ``ModelAdmin`` classes.

    Example:
        class TestSampleModelAdminFields(TestAdminFieldsMixin, TestCase):
            factory = SampleModelFactory
            model_admin = SampleModelAdmin

    """

    def test_model_admin_fields(self):
        """Test for correct implementation of Model Admin.

        Checks if fields, specified in Model Admin, are also specified in
        Model class itself.

        """
        try:
            self.get_admin_instance().get_form(self._get_request())
        except FieldError as e:
            admin = self.model_admin
            model = self.get_model()
            msg = (
                '\'{0}\' fieldset is not relevant to \'{1}\' model.\n{2}'
                .format(admin.__name__, model.__name__, e)
            )
            raise AssertionError(msg) from None

    def _get_request(self):
        """Shortuct for mocking request object"""
        request = self._factory.get('/')
        setattr(request, 'META', {'QUERY_STRING': ''})
        return request


class TestRelatedObjectActionsMixin(AdminTestShortcuts):
    """Mixin for testing `RelatedObjectActionsMixin`.

    Example:
        class EventAdminTest(TestRelatedObjectActionsMixin, TestCase):
            factory = EventFactory
            model_admin = EventAdmin

    Applied in schedule admin tests
    """

    def test_related_admin_links(self):
        """Test for `RelatedObjectActionsMixin`.

        Ensure that links to related object actions are stored in response.

        """
        self.client.force_login(AdminUserFactory())
        obj = self.factory()
        url = self.get_change_view_url(obj)
        response_html = self.client.get(url).rendered_content

        for related_model in self.get_admin_instance().related_models:
            expected_html = 'title="{}"'.format(
                related_model._meta.verbose_name_plural
            )
            self.assertIn(expected_html, response_html)


class TestInitialValuesAdminMixin(AdminTestShortcuts):
    """Mixin for testing `InitialValuesAdminMixin`.

    Example:
        class TestDiscussionThreadAdmin(TestInitialValuesAdminMixin, TestCase):
            factory = DiscussionThreadFactory
            model_admin = DiscussionThreadAdmin
            field_with_initial_value = 'module'

    Applied in schedule admin tests

    """
    field_with_initial_value = None

    def setUp(self):
        super().setUp()
        assert self.field_with_initial_value, (
            '`field_with_initial_value` attribute is not specified.'
        )

    def test_initial_values_in_admin(self):
        """Test for `InitialValuesAdminMixin`.

        Ensure that `Add object` page contains pre-selected attribute.

        """
        # Create new instance and get it's investigated attribute
        instance = self.factory()
        attribute = self._get_field_attribute(instance)

        # Create request to `Add object` page
        filtered_url = self._get_filtered_url(attribute)
        request = RequestFactory().get(filtered_url)

        # Get admin form using created request and get specified field
        admin_form = self.get_admin_instance().get_form(request)
        admin_field = admin_form.base_fields[self.field_with_initial_value]

        # Assert that field initial value is equal to specified instance
        self.assertEqual(admin_field.initial, attribute)

    def _get_field_attribute(self, obj):
        """Shortcut to get `field_with_initial_value` attribute for `obj`."""
        return getattr(obj, self.field_with_initial_value)

    def _get_filtered_url(self, attribute):
        """Method to get URL for `Add object` admin page with filter."""
        # Get URL for `Add object` page
        url = self.get_add_view_url()

        # Manually add `changelist_filters` to URL
        field = self._get_field_attribute(self.get_model()).field
        params_dict = field.get_forward_related_filter(attribute)

        # {'module__module_ptr': 123} -> 'module__module_ptr__exact=123'
        params_str = ''.join(
            '{}__exact={}'.format(key, val) for key, val in params_dict.items()
        )

        # Create new URL using original URL and `changelist_filters`
        changelist_filters = '?_changelist_filters={}'.format(params_str)
        return url + changelist_filters


class TestDisabledFieldsMixin(AdminTestShortcuts):
    """Mixin for testing  ``DisabledFieldsMixin``.

    Example:
        class TestDiscussionThreadAdmin(TestDisabledFieldsMixin, TestCase):
            factory = DiscussionThreadFactory
            model_admin = DiscussionThreadAdmin

    Applied in schedule admin tests
    """

    def test_fields_are_enabled_for_new_obj(self):
        """Test that `disabled_fields` are enabled in add view."""
        url = self.get_add_view_url()
        request = RequestFactory().get(url)
        admin_form = self.get_admin_instance().get_form(request, None)
        self.assertFieldsAreDisabled(admin_form, False)

    def test_fields_are_disabled_for_existing_obj(self):
        """Test that `disabled_fields` are disabled in change view."""
        obj = self.factory()
        url = self.get_change_view_url(obj)
        request = RequestFactory().get(url)
        admin_form = self.get_admin_instance().get_form(request, obj)
        self.assertFieldsAreDisabled(admin_form, True)

    def assertFieldsAreDisabled(self, form, are_disabled):
        """Check if widget for `disabled_fields` is disabled/enabled."""
        for field in self.model_admin.disabled_fields:
            field = form.base_fields[field]
            self.assertEqual(field.disabled, are_disabled)
