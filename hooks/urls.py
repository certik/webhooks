from django.conf.urls.defaults import *

urlpatterns = patterns('webhooks.hooks.views',
    (r'^$', 'index'),
)
