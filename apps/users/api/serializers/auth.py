from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from allauth.account.forms import ResetPasswordForm
from rest_auth import serializers as ras
from rest_auth.registration.serializers import RegisterSerializer

from libs.api.serializers.fields import DateTimeFieldWithTZ
from libs.api.serializers.serializers import LocationSerializer


class CustomRegisterSerializer(RegisterSerializer):
    """ You can add any extra fields to registration. Example:
    first_name = serializers.CharField()

    def get_cleaned_data(self):
        cleaned_data = super().get_cleaned_data()
        cleaned_data.update({
                'first_name': self.validated_data['first_name'],
            })
        return cleaned_data
    """
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    # gender = serializers.CharField(required=False)
    # city = serializers.CharField(required=False)
    # state = serializers.CharField(required=False)
    # about = serializers.CharField(required=False)

    def get_cleaned_data(self):
        """Solution to persist more data during allauth
        registration API call. Not the 'nicest' way, but
        probably the only 'easy' way
        """
        cleaned_data = super().get_cleaned_data()
        cleaned_data.update({
            'first_name': self.validated_data['first_name'],
            'last_name': self.validated_data['last_name'],
            # 'gender': self.validated_data.get('gender', None),
            # 'city': self.validated_data.get('city', None),
            # 'state': self.validated_data.get('state', None),
            # 'about': self.validated_data.get('about', None)
        })
        return cleaned_data


class CustomPasswordResetSerializer(ras.PasswordResetSerializer):
    password_reset_form_class = ResetPasswordForm

    def validate_email(self, email):
        self.reset_form = self.password_reset_form_class(
            data=self.initial_data
        )
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(
                'The e-mail address is not assigned to any user account'
            )
        return email


class CustomPasswordResetConfirmSerializer(ras.PasswordResetConfirmSerializer):
    """Custom password reset confirm serializer."""

    def validate(self, attrs):
        """Method to validate serializer.

        This method is identical to original `validate` method but without
        `uid` format validation, because `User` model id is not an uuid.

        """
        User = get_user_model()
        self._errors = {}

        try:
            # Removed uid format validation in this line
            self.user = User.objects.get(pk=attrs['uid'])
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise ValidationError({'uid': ['Invalid value']})

        self.custom_validation(attrs)
        # Construct SetPasswordForm instance
        self.set_password_form = self.set_password_form_class(
            user=self.user,
            data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)
        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs


class CustomUserDetailSerializer(serializers.ModelSerializer):

    location_updated = DateTimeFieldWithTZ(read_only=True)
    location = LocationSerializer(read_only=True)
    date_joined = DateTimeFieldWithTZ(read_only=True)
    last_login = DateTimeFieldWithTZ(read_only=True)

    class Meta:
        model = get_user_model()
        depth = 1
        exclude = (
            'password',
            'is_superuser',
            'is_staff',
            'is_active',
            'groups',
            'user_permissions'
        )
        read_only_fields = ('email', 'username', )
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': False},
            'location': {'read_only': False, 'required': False},
        }


class CustomUserManageableSerializer(serializers.ModelSerializer):
    """Allow to edit user information"""
    location_updated = DateTimeFieldWithTZ(read_only=True)
    location = LocationSerializer(read_only=True)
    date_joined = DateTimeFieldWithTZ(read_only=True)
    last_login = DateTimeFieldWithTZ(read_only=True)

    class Meta:
        model = get_user_model()
        depth = 1
        exclude = (
            'password',
        )
        read_only_fields = ('balance',)
