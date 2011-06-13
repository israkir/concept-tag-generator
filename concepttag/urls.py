from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^app_generator/$', 'concepttag.app_generator.views.articleInput'),
    #(r'^app_generator/articleInput/$', 'concepttag.app_generator.views.articleInput'),
    (r'^app_generator/keywordsGenerator/$', 'concepttag.app_generator.views.keywordsGenerator'),
    (r'^app_generator/keywordsFeedback/$', 'concepttag.app_generator.views.keywordsFeedback'),
    
    # Example:
    # (r'^concepttag/', include('concepttag.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
