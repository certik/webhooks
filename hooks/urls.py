from django.conf.urls.defaults import *

urlpatterns = patterns('hooks.views',
    (r'^$', 'index'),
    (r'^users/$', 'users'),
    (r'^users/(?P<user>\S+)/$', 'user'),
    (r'^repos/$', 'repos'),
    (r'^repos/add/$', 'repo_add'),
    (r'^repos/delete/(?P<repo>\S+)/$', 'repo_delete'),
    (r'^repos/(?P<repo>\S+)/$', 'repo'),
    (r'^worker/authors/$', 'worker_authors'),
    (r'^worker/user_email/$', 'worker_email'),
)
