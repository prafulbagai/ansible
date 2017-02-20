
import views

from django.conf.urls import url

urlpatterns = [
    url(r'^refresh_cache/?$', views.CacheRefresh.as_view(), name='refresh_cache'),
]
