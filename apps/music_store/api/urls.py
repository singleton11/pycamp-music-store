from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter

from apps.music_store.api import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'albums', views.AlbumViewSet)
router.register(r'tracks', views.TrackViewSet)
router.register(r'likes', views.LikeTrackViewSet)
# router.register(r'putlikes', views.LikeSomeTrackAPIView)
router.register(r'listens', views.ListenTrackViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    url(r'^put_likes/$',
        views.LikeSomeTrackAPIView.as_view(),
        name='like'),

    url(r'^', include(router.urls)),
]
