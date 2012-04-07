from django.conf.urls.defaults import *
from django.conf import settings
from zero.company import views

urlpatterns = patterns('',
    url(r'^$', views.list, name='company-list'),
    url(r'^movers/(\d+)/(\d+)/(\d+)$', views.movers, name='company-movers'),
    url(r'^ohlc/([\w\.:]*)/(\d*)$', views.ohlc, name='company-ohlc'),
    url(r'^([\w\.:]*)$', views.details, name='company-details'),
)
