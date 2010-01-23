from django.conf import settings
from django.conf.urls.defaults import *
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.simple import direct_to_template

from django.contrib import admin
admin.autodiscover()



# override the default handler500 so i can pass MEDIA_URL
handler500 = "company_project.views.server_error"


def static_view(request, path):
    """
    serve pages directly from the templates directories.
    """
    if not path or path.endswith("/"):
        template_name = path + "index.html"
    else:
        template_name = path
    return render_to_response(template_name, RequestContext(request))


def noop(request):
    pass


urlpatterns = patterns("",
    url(r"^$", direct_to_template, {"template": "homepage.html"}, name="home"),
    
    url(r"^blog/", include("biblion.urls")),
    url(r"^feed/$", "biblion.views.blog_feed", name="blog_feed_combined"),
    url(r"^feed/(?P<section>[-\w]+)/$", "biblion.views.blog_feed", name="blog_feed"),
    
    # stubbed out for reverse (webserver maps this to static file serving)
    url(r"^docs/$", noop, name="documentation"),
    
    url(r"^sites/", include("example_sites.urls")),
    url(r"^quotes/", include("quotes.urls")),
    url(r"^events/", include("events.urls")),
    
    url(r"^admin/(.*)", admin.site.root),
)


if settings.SERVE_MEDIA:
    urlpatterns += patterns("",
        (r"", include("staticfiles.urls")),
    )


urlpatterns += patterns("",
    (r"^(.*)$", static_view),
)