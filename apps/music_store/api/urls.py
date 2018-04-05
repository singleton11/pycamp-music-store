from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.music_store.api.views import (
    PaymentAccountViewSet,
    PaymentMethodViewSet,
    BoughtTrackView,
)

router = DefaultRouter()
router.register(r'payment_methods', PaymentMethodViewSet)
router.register(r'payment_accounts', PaymentAccountViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^bought_tracks/$', BoughtTrackView.as_view()),
]
