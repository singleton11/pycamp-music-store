from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apps.music_store.api.views import (
    PaymentAccountView,
    PaymentMethodViewSet,
    BoughtTrackView,
)

router = DefaultRouter()
router.register(r'payment_methods', PaymentMethodViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^bought_tracks/$', BoughtTrackView.as_view()),
    url(r'^payment_account/$', PaymentAccountView.as_view()),
]
