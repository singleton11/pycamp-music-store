# Rest framework API configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # SessionAuthentication is also used for CSRF
        # validation on ajax calls from the frontend
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_MODEL_SERIALIZER_CLASS':
        'rest_framework.serializers.ModelSerializer',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'EXCEPTION_HANDLER':
        'libs.api.exceptions.custom_exception_handler_simple'
}

REST_FRAMEWORK_CUSTOM_FIELD_MAPPING = {
    # Additional fields mappings
    # Configure updating ``ModelSerializer.serializer_field_mapping`` dict
    # When ``libs.apps.LibsAppConfig`` executes
    'django.contrib.gis.db.models.PointField':
        'libs.api.serializers.fields.CustomLocationField',
    'django.db.models.DateTimeField':
        'libs.api.serializers.fields.DateTimeFieldWithTZ'
}

# Django Rest Auth (Rest API Layer) above allauth

REST_AUTH_SERIALIZERS = {
    'PASSWORD_RESET_SERIALIZER':
        'apps.users.api.serializers.auth.CustomPasswordResetSerializer',
    'USER_DETAILS_SERIALIZER':
        'apps.users.api.serializers.auth.CustomUserDetailSerializer',
    'PASSWORD_RESET_CONFIRM_SERIALIZER':
        'apps.users.api.serializers.auth.CustomPasswordResetConfirmSerializer',
}

REST_AUTH_REGISTER_SERIALIZERS = {
    'REGISTER_SERIALIZER':
        'apps.users.api.serializers.auth.CustomRegisterSerializer',
}
