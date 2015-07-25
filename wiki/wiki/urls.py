from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'wiki.views.home_page', name='home_page'),
    url(r'^login/$', 'wiki.views.login_user', name='login_user'),
    url(r'^logout/$', 'wiki.views.logout_user', name='logout_user'),
    url(r'^view/(?P<slug>[^\.]+).html$', 'wiki.views.view_page', name='view_page'),
    url(r'^edit/(?P<slug>[^\.]+).html$', 'wiki.views.edit_page', name='edit_page'),
    url(r'^save/(?P<slug>[^\.]+).html$', 'wiki.views.save_page', name='save_page'),
    # url(r'^search/', include('haystack.urls')),
    # url(r'^edit/(?P<slug>[^\.]+).html$', 'blog.views.edit', name='edit'),
]
