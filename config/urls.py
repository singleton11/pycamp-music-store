from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

from rest_auth.registration.views import RegisterView

urlpatterns = [
    # ADMIN urls
    url(r'^admin/', admin.site.urls),

    # API endpoints
    url(r'^api/v1/auth/', include('rest_auth.urls')),
    url(r'^api/v1/auth/register', RegisterView.as_view()),
    url(r'^api/v1/oauth/', include('apps.users.api.oauth_urls')),
    url(r'^api/v1/', include('apps.users.api.urls')),

    url(r'^users/', include('apps.users.urls')),
    url(r'^api/v1/music_store/', include('apps.music_store.api.urls')),
]

# for serving uploaded files on dev environment with django
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

# adding urls for demonstration or fake apps
# this code adds urls for fake apps to this endpoints:
#   for web UI:
#      /demo/{application_label}/
#   for API:
#      /api/v1/demo/{application_label}/
# if you want to add your fake application, you should
# inherit your application config from libs.apps.FakeAppConfig and
# define property app_urls and api_urls with paths to your urls modules.
if settings.TESTING or settings.DEBUG:
    from django.apps import apps
    from libs.apps import is_fake_app

    for app_label, app_config in apps.app_configs.items():
        # we works here just with fake applications
        if not is_fake_app(app_config):
            continue

        # adding application urls
        url_path = r'^demo/{}/'.format(app_label)
        if app_config.app_urls:
            urlpatterns += [url(url_path, include(app_config.app_urls))]

        # adding API urls
        api_urls_path = r'^api/v1/demo/{}/'.format(app_label)
        if app_config.api_urls:
            urlpatterns += [url(api_urls_path, include(app_config.api_urls))]
