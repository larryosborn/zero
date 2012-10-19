from django.conf.urls.defaults import *
from django.conf import settings
from zero.company import views

urlpatterns = patterns('',
    url(r'^api/list', views.api_list, name='api-company-list'),
    url(r'^api/ohlc/([\w\.:]*)/(\d*)$', views.api_ohlc, name='api-company-ohlc'),
    url(r'^api/indexes$', views.api_index_list, name='api-company-indexes'),
    url(r'^api/index/(.+)$', views.api_index, name='api-company-index'),
    url(r'^api/sectors$', views.api_sector_list, name='api-company-sectors'),
    url(r'^api/sector/(.+)$', views.api_sector, name='api-company-sector'),

    url(r'^$', views.list, name='company-list'),
    url(r'^indexes$', views.index_list, name='index-list'),
    url(r'^index/(.+)$', views.index, name='index'),
    url(r'^sectors$', views.sector_list, name='sector-list'),
    url(r'^sector/(.+)$', views.sector, name='sector'),
    url(r'^movers/(\d+)/(\d+)/(\d+)$', views.movers, name='company-movers'),
    url(r'^movers$', views.movers_today, name='company-movers-today'),
    url(r'^([\w\.:]*)$', views.details, name='company-details'),

)
