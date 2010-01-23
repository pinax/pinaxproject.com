from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template



urlpatterns = patterns("",
    url(r"^$", direct_to_template, {
        "template": "sites.html",
    }, name="sites_home"),
    url(r"^submit/$", "example_sites.views.submit_site", name="sites_submit_site"),
)