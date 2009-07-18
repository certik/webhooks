from django.conf.urls.defaults import *

urlpatterns = patterns('hooks.views',
    (r'^$', 'index'),
    (r'^users/$', 'users'),
    (r'^users/(?P<user>\S+)/$', 'user'),
    (r'^repos/$', 'repos'),
    (r'^repos/(?P<repo>\S+)/$', 'repo'),
    (r'^worker/authors/$', 'worker_authors'),
)
