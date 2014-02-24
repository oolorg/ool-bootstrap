from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
	(r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'index.html'}),
	(r'^cgi-bin/index.py', 'bootstrap.web.cgi-bin.index.start'),
        (r'^cgi-bin/edit_credentials.py', 'bootstrap.web.cgi-bin.edit_credentials.start'),
	(r'^cgi-bin/build_scenario.py', 'bootstrap.web.cgi-bin.build_scenario.start'),
	(r'^cgi-bin/edit_scenario.py', 'bootstrap.web.cgi-bin.edit_scenario.start'),
	(r'^cgi-bin/build_exec.py', 'bootstrap.web.cgi-bin.build_exec.start'),
	(r'^cgi-bin/view_log.py', 'bootstrap.web.cgi-bin.view_log.start'),
	(r'^cgi-bin/scenario_delete.py', 'bootstrap.web.cgi-bin.scenario_delete.start'),
	(r'^cgi-bin/scenario_result.py', 'bootstrap.web.cgi-bin.scenario_result.start'),
	(r'^cgi-bin/show_environment.py', 'bootstrap.web.cgi-bin.show_environment.start'),
	(r'^cgi-bin/urlRequest.py', 'bootstrap.web.cgi-bin.urlRequest.start'),
	(r'^cgi-bin/show_result.py', 'bootstrap.web.cgi-bin.show_result.start'),
    # Examples:
    # url(r'^$', 'bootstrap.views.home', name='home'),
    # url(r'^bootstrap/', include('bootstrap.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += staticfiles_urlpatterns()
