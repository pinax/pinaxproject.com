from django.conf.urls.defaults import patterns, url


urlpatterns = patterns("",
    url(r"^$", "downloads.views.download_index", name="download_index"),
)