
from django.conf.urls import url
from django.views.generic import TemplateView

from allauth.account import views as account_views
from allauth.socialaccount import views as social_views


urlpatterns = [
    url('^signup/$', social_views.signup, name='socialaccount_signup'),
    url(r"^email-confirmed/$",
        TemplateView.as_view(template_name='account/email_confirmed.html'),
        name="account_email_confirmed"),
    url(r"^confirm-email/(?P<key>\w+)/$", account_views.confirm_email,
        name="account_confirm_email"),
    url(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
        account_views.password_reset_from_key,
        name="account_reset_password_from_key"),
    url(r"^password/reset/key/done/$",
        account_views.password_reset_from_key_done,
        name="account_reset_password_from_key_done"),
]


