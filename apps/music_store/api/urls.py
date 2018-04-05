from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.music_store.api.views import (
    AccountView,
    PaymentMethodViewSet,
    BoughtTrackViewSet,
    BoughtAlbumViewSet
)

router = DefaultRouter()
router.register(r'payment_methods', PaymentMethodViewSet)
router.register(r'bought_tracks', BoughtTrackViewSet)
router.register(r'bought_albums', BoughtAlbumViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^account/$', AccountView.as_view()),
]
