from django.conf.urls import url, include

urlpatterns = [
    url(r'^$', 'wiki.views.home_page', name='home_page'),
    url(r'^login/$', 'wiki.views.login_user', name='login_user'),
    url(r'^logout/$', 'wiki.views.logout_user', name='logout_user'),
    url(r'^view/(?P<slug>[^\.]+).html$', 'wiki.views.view_page', name='view_page'),
    url(r'^edit/(?P<slug>[^\.]+).html$', 'wiki.views.edit_page', name='edit_page'),
    url(r'^save/(?P<slug>[^\.]+).html$', 'wiki.views.save_page', name='save_page'),
    url(r'^history/(?P<slug>[^\.]+).html$', 'wiki.views.page_history', name='page_history'),
    url(r'^history/(?P<slug>[^\.]+)/(?P<version_id>[0-9]+)$', 'wiki.views.page_change', name='page_change'),
    url(r'^search/', include('haystack.urls')),
    url(r'^delete/$', 'wiki.views.delete_page', name='delete_page'),
]
