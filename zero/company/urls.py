from django.conf.urls.defaults import *
from django.conf import settings
from zero.company import views

urlpatterns = patterns('',
    url(r'^$', views.list, name='list-view'),
    url(r'^stats/([\w\.:]*)/(\d*)$', views.stats, name='stats-view'),
    url(r'^ohlc/([\w\.:]*)/(\d*)$', views.ohlc, name='ohlc-view'),
    url(r'^([\w\.:]*)$', views.details, name='details-view'),
)
