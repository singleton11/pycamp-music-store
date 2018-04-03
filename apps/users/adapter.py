from contextlib import suppress

from django.conf import settings
from django.db.models import Q

from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.models import EmailAddress
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    """Custom account adapter.

    Used for association social accounts with existiong users.

    Source: https://goo.gl/2Q7247

    """

    def pre_social_login(self, request, sociallogin):
        verified_email = None
        verification = False

        with suppress(AttributeError):
            verification = settings.ACCOUNT_EMAIL_VERIFICATION == 'mandatory'

        # some social logins don't have an email address
        if not sociallogin.email_addresses:
            return

        # find the first verified email that we get from this sociallogin
        # if verification is enabled in settings, else get first email
        for email in sociallogin.email_addresses:
            if (verification and email.verified) or not verification:
                verified_email = email
                break

        # no verified emails found, nothing more to do
        if not verified_email:
            return

        # check if given email address already exists as a verified email on
        # an existing user's account
        try:
            qs = Q(email__iexact=email.email)

            if verification:
                qs = qs & Q(verified=True)

            existing_email = EmailAddress.objects.get(qs)
        except EmailAddress.DoesNotExist:
            return

        # if it does, connect this new social login to the existing user
        sociallogin.connect(request, existing_email.user)


class AccountAdapter(DefaultAccountAdapter):
    """
    Adapter to store additional fields on registration
    Adjust it if you need custom fields saved during user
    registration call
    http://django-allauth.readthedocs.org/en/latest/advanced.html#creating-and-populating-user-instances
    """

    def save_user(self, request, user, form):
        """
        Args:
            user (users.AppUser): empty AppUser instance
            form (CustomRegisterSerializer): Serializer filled with values
        """
        # user.gender = form.validated_data.get('gender', None)
        # user.city = form.validated_data.get('city', None)
        # user.state = form.validated_data.get('state', None)
        # user.about = form.validated_data.get('about', None)
        return super().save_user(request, user, form)
