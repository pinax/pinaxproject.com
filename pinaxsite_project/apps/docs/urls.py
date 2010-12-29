from django.conf.urls.defaults import *


urlpatterns = patterns("",
    url(r"^$", "docs.views.documentation_index", name="documentation_index"),
    url(r"^(?P<version>[\w\.]+)/$", "docs.views.documentation_detail", name="documentation_version"),
    url(r"^(?P<version>[\w\.]+)/(?P<slug>[\w\.-\/]+\.html)$", "docs.views.documentation_detail"),
    url(r"^(?P<version>[\w\.]+)/(?P<slug>[\w\.-\/]+)/$", "docs.views.documentation_detail", name="documentation_detail"),
)