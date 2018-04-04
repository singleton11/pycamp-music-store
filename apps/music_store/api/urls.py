from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.music_store.api.views import PaymentAccountViewSet, PaymentMethodViewSet, BoughtTrackViewSet

router = DefaultRouter()
router.register(r'payment_methods', PaymentMethodViewSet)
router.register(r'payment_accounts', PaymentAccountViewSet)
router.register(r'bought_tracks', BoughtTrackViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
