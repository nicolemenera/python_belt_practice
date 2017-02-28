from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^addplan$', views.addplan),
    url(r'^settrip$', views.settrip),
    url(r'^logout$', views.logout),
    url(r'^join/(?P<trip>\d+)$', views.join),
    url(r'^description/(?P<tripid>\d+)$', views.description)
    
]