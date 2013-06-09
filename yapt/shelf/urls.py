from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
		url(r'^$', 'shelf.views.home'),
		url(r'^addArticle/$', 'shelf.views.addArticle'),
		url(r'^home/$', 'shelf.views.home'),
		url(r'^search/$', 'shelf.views.search', {'filter_name' : 'all'}),
		url(r'^search/([a-zA-z0-9]+)$', 'shelf.views.search', name='search'),
		url(r'^editArticle/(\d+)/$', 'shelf.views.edit_article', name='edit'),
)
