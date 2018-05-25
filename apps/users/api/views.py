from django.contrib.auth import get_user_model
from django.http import Http404

from rest_framework import generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from allauth.socialaccount.providers.facebook.views import (
    FacebookOAuth2Adapter,
)
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

from libs.api.serializers.serializers import (
    LocationSerializer,
    UploadSerializer,
)

from .serializers import auth

AppUser = get_user_model()


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter


class UserUploadAvatarAPIView(
        generics.CreateAPIView,
        generics.DestroyAPIView,
        generics.GenericAPIView
):
    permission_classes = (IsAuthenticated,)
    serializer_class = UploadSerializer

    def create(self, request, *args, **kwargs):
        """Upload avatar to remote storage"""
        serializer = self.get_serializer(data=self.request.data)

        serializer.is_valid(raise_exception=True)
        user = self.request.user
        upload = serializer.validated_data['upload']
        field = user.avatar
        field.delete()
        field.save(upload.name, upload)

        return Response(
            {'url': field.url},
            status=status.HTTP_201_CREATED
        )

    def delete(self, request, *args, **kwargs):
        """Delete avatar from remote storage"""
        user = self.request.user
        if user.avatar:
            user.avatar.delete()
            user.save()
        return Response(status=status.HTTP_200_OK)


class UserGeoLocationAPIView(APIView):
    """Geo location endpoint
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = LocationSerializer

    def post(self, request):
        # get current user
        user = self.request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user)
        return Response(status=status.HTTP_201_CREATED)


class CheckUsernameView(APIView):
    """
    Used to check availability of username
    """

    def get(self, request, username):
        UserModel = get_user_model()
        params = {
            '{0}__iexact'.format(UserModel.USERNAME_FIELD): username
        }
        qs = get_user_model().objects.filter(**params)
        if not qs.exists():
            raise Http404
        return Response(status=status.HTTP_200_OK)


class UsersViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing and editing accounts.
    """
    queryset = AppUser.objects.all()
    serializer_class = auth.CustomUserDetailSerializer
    permission_classes = [AllowAny]


class UsersManageableViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Admin viewing and editing accounts.
    """
    queryset = AppUser.objects.exclude(id=1)
    serializer_class = auth.CustomUserManageableSerializer
    permission_classes = [IsAdminUser]


class LookupUserOptionsView(APIView):
    """
    Lookup class for getting list of available users
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        """
        Return a list of all users.
        """
        usernames = {
            user.username: user.username.title()
            for user in AppUser.objects.all()}
        return Response(usernames)
