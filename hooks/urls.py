from django.conf.urls.defaults import *

urlpatterns = patterns('hooks.views',
    (r'^$', 'index'),
    (r'^users/$', 'users'),
)
