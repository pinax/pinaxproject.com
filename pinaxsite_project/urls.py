from django.conf import settings
from django.conf.urls.defaults import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()



handler500 = "pinax.views.server_error"


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "homepage.html"}, name="home"),
    
    url(r"^blog/", include("biblion.urls")),
    url(r"^feed/$", "biblion.views.blog_feed", name="blog_feed_combined"),
    url(r"^feed/(?P<section>[-\w]+)/$", "biblion.views.blog_feed", name="blog_feed"),
    url(r"^docs/", include("docs.urls")),
    
    url(r"^downloads/", include("downloads.urls")),
    url(r"^sites/", include("example_sites.urls")),
    url(r"^quotes/", include("quotes.urls")),
    url(r"^events/$", direct_to_template, {
        "template": "events/home.html",
    }, name="events_home"),
    
    url(r"^admin/", include(admin.site.urls)),
    
    url(r"^packages/", include("packages.urls")),
    
    # temporary urls
    url(r"^docs/$", direct_to_template, {"template": "docs/index.html"}, name="index"),
    url(r"^docs/dev/$", direct_to_template, {"template": "docs/dev_index.html"}, name="dev_index"),
    url(r"^docs/dev/gettingstarted/$", direct_to_template, {"template": "docs/detail.html"}, name="gettingstarted"),
    
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        url(r"", include("staticfiles.urls")),
    )


if settings.DEBUG:
    urlpatterns += patterns("",
        (r"^(.*)$", "pinax.views.static_view"),
    )