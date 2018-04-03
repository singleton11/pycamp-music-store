from django.conf.urls import url

from apps.users.api.views import FacebookLogin, GoogleLogin

urlpatterns = [
    url(r'^facebook/$', FacebookLogin.as_view(), name='fb_login'),
    url(r'^google/$', GoogleLogin.as_view(), name='ggl_login'),
]
