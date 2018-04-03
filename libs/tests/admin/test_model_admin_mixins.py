from unittest.mock import patch

from django.contrib import admin
from django.db import models
from django.forms import ModelForm
from django.test import TestCase

from ...admin.mixins.model_admin import (
    AllFieldsReadOnly,
    FkAdminLink,
    ForbidDeleteAdd,
)


class ForbidDeleteAddTestCase(TestCase):
    """Test case for ``ForbidDeleteAdd`` admin model mixin"""

    def setUp(self):
        self.forbid_delete_add = ForbidDeleteAdd()

    def test_has_delete_permission(self):
        """``has_delete_permission`` should always return ``False``"""
        self.assertFalse(self.forbid_delete_add.has_delete_permission(None))

    def test_has_add_permission(self):
        """``has_add_permission`` should always return ``False``"""
        self.assertFalse(self.forbid_delete_add.has_add_permission(None))


class Post(models.Model):
    """Test model for ``FkAdminLinkTestCase``"""
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title


class PostForm(ModelForm):
    """Test form to check extending field excluding in
     ``AllFieldsReadOnlyTestCase``"""

    class Meta:
        model = Post
        exclude = ['title']


class FkAdminLinkTestCase(TestCase):
    """Test case for admin link mixin ``FkAdminLink``"""

    @patch('django.core.urlresolvers.RegexURLResolver._reverse_with_prefix', return_value='test')
    def test_admin_url(self, reverse):
        """Test for related object link generation"""
        post = Post(title='title', text='test')
        fk_admin_link = FkAdminLink()
        # Assert without title
        self.assertEqual(
            fk_admin_link._admin_url(post),
            "<a href='test' target='_blank'>title</a>"
        )
        # Assert when title transfered to ``_admin_url``
        self.assertEqual(
            fk_admin_link._admin_url(post, 'test'),
            "<a href='test' target='_blank'>test</a>"
        )


class AllFieldsReadOnlyTestCase(TestCase):
    """Test case for ``AllFieldsReadOnly`` mixin"""

    def setUp(self):
        class PostAdmin(AllFieldsReadOnly, admin.ModelAdmin):
            pass

        class PostAdminWithFieldsAttr(AllFieldsReadOnly, admin.ModelAdmin):
            fields = ['test_field']

        class PostAdminWithExcludeField(AllFieldsReadOnly, admin.ModelAdmin):
            exclude = ['title']

        class PostAdminWithExcludeFieldInForm(
            AllFieldsReadOnly,
            admin.ModelAdmin
        ):
            form = PostForm

        self.post_admin = PostAdmin(Post, admin.AdminSite())
        self.post_admin_with_fields_attr = PostAdminWithFieldsAttr(
            Post,
            admin.AdminSite()
        )
        self.post_admin_with_exclude_field = PostAdminWithExcludeField(
            Post,
            admin.AdminSite()
        )
        self.post_admin_exclude_field_in_form = \
            PostAdminWithExcludeFieldInForm(Post, admin.AdminSite())

    def test_get_readonly_fields(self):
        """Test ``get_readonly_fields`` should return all fields of model"""
        self.assertEqual(
            self.post_admin.get_readonly_fields(None),
            ['title', 'text']
        )

    def test_get_readonly_fields_with_fields_attr(self):
        """Test ``get_readonly_fields`` with ``fields`` attribute, should return
        attribute value"""
        self.assertEqual(
            self.post_admin_with_fields_attr.get_readonly_fields(None),
            ['test_field']
        )

    def test_get_readonly_fields_with_exclude_fields(self):
        """Test ``get_readonly_fields`` with ``exclude`` attribute, should not
        return fields which points in ``exclude``"""
        self.assertEqual(
            self.post_admin_with_exclude_field.get_readonly_fields(None),
            ['text']
        )

    def test_get_readonly_fields_with_exclude_fields_in_form(self):
        """Test ``get_readonly_fields`` with ``exclude`` attribute in ``Meta``
        class in form which defined in admin class"""
        self.assertEqual(
            self.post_admin_exclude_field_in_form.get_readonly_fields(None),
            ['text']
        )
