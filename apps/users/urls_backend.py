from django.conf.urls import url

from .views import DashboardView

# Backend URLs
urlpatterns = [
    url(r'', DashboardView.as_view(), name='dashboard'),
    url(r'^dashboard/', DashboardView.as_view(), name='dashboard'),
]
