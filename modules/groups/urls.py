
import views

from django.conf.urls import url

urlpatterns = [
    url(r'^api/groups/?$', views.GroupsView.as_view(), name='groups'),
    url(r'^api/group/details?$', views.GroupsView.as_view(), name='group_details'),
]
