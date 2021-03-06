from django.conf.urls.defaults import url, patterns

from packages.views import AppList, StarterProjectList, ThemeList
from packages.views import PackageList, PackageDetail, CommitsView
from packages.views import PullRequestList, DashboardView


urlpatterns = patterns("",
    url(r"^$", PackageList.as_view(), name="packages_list"),
    url(r"commits/$", CommitsView.as_view(), name="packages_commits"),
    url(r"^(?P<pk>\d+)/$", PackageDetail.as_view(), name="packages_detail"),
    
    url(r"^apps/$", AppList.as_view(), name="packages_app_list"),
    url(r"^starter_projects/$", StarterProjectList.as_view(), name="packages_starter_projects_list"),
    url(r"^themes/$", ThemeList.as_view(), name="packages_theme_list"),
    url(r"^pull-requests/$", PullRequestList.as_view(), name="packages_pull_requests"),
    url(r"^dashboard/$", DashboardView.as_view(), name="packages_dashboard"),
)
