from django.conf.urls import url

from rest_framework.routers import DefaultRouter

from .views import (
    CheckUsernameView,
    LookupUserOptionsView,
    UserGeoLocationAPIView,
    UsersViewSet,
    UserUploadAvatarAPIView,
)

# register URL like
# router.register(r'users', UsersAPIView)
router = DefaultRouter()
router.register(r'users', UsersViewSet, base_name='user')
urlpatterns = router.urls

urlpatterns += [
    url(r'^user/location/$', UserGeoLocationAPIView.as_view()),
    url(r'^user/avatar/$', UserUploadAvatarAPIView.as_view()),
    url(r'^check/(?P<username>.*)/$', CheckUsernameView.as_view()),
    url(r'^lookup/users/$', LookupUserOptionsView.as_view()),
]
