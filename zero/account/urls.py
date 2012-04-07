from django.conf.urls.defaults import *
from django.conf import settings
from zero.account import views

urlpatterns = patterns('',
    url(r'^details$', views.details, name='account-details'),
    url(r'^transaction$', views.transaction, name='transaction-view'),
)
