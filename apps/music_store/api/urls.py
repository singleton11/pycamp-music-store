from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from ..api import views

router = DefaultRouter()
router.register(r'albums', views.AlbumViewSet)
router.register(r'bought_albums', views.BoughtAlbumViewSet)
router.register(r'bought_tracks', views.BoughtTrackViewSet)
router.register(r'tracks', views.TrackViewSet)
router.register(r'likes', views.LikeTrackViewSet)
router.register(r'listens', views.ListenTrackViewSet)
router.register(r'payment_methods', views.PaymentMethodViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^account/$', views.AccountView.as_view()),
]
