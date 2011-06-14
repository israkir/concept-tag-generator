from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'concepttag.app_generator.views.articleInput'),
    # (r'^articleInput/$', 'concepttag.app_generator.views.articleInput'),
    (r'^keywordsGenerator/$', 'concepttag.app_generator.views.keywordsGenerator'),
    (r'^keywordsFeedback/$', 'concepttag.app_generator.views.keywordsFeedback'),
)
