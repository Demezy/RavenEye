from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.base, name='base'),
    url(r'^index/$', views.index, name='index'),
    url(r'^panel/$', views.panel, name='panel'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^video_feed/$', views.video_feed, name='video_feed'),
]
