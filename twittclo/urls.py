from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'twittclo_app.views.index'), # root
    url(r'^login$', 'twittclo_app.views.login_view'), # login
    url(r'^logout$', 'twittclo_app.views.logout_view'), # logout
    url(r'^signup$', 'twittclo_app.views.signup'), # signup
    url(r'^twittclos$', 'twittclo_app.views.public'), # public twitts
    url(r'^submit$', 'twittclo_app.views.submit'), # submit new twittclo
    url(r'^users/$', 'twittclo_app.views.users'),
    url(r'^users/(?P<username>\w{0,30})/$', 'twittclo_app.views.users'),
    url(r'^follow$', 'twittclo_app.views.follow'),
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    #url(r'^admin/', include(admin.site.urls)),
)