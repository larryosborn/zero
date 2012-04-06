from django.conf.urls.defaults import *
from django.conf import settings
from zero.account import views

urlpatterns = patterns('',
    (r'^details$', views.details),
    (r'^transaction$', views.transaction),
)
