import datetime

from math import log

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from packages.models import Package, Commit, PullRequest, final_months
from packages.models import CommitsByPackageByMonth, CommitsByAuthorByMonth


class AppList(ListView):
    
    template_name = "packages/list.html"
    queryset = Package.apps().order_by("name")
    context_object_name = "packages"


class StarterProjectList(ListView):
    
    template_name = "packages/list.html"
    queryset = Package.starter_projects().order_by("name")
    context_object_name = "packages"


class ThemeList(ListView):
    
    template_name = "packages/list.html"
    queryset = Package.themes().order_by("name")
    context_object_name = "packages"


class PackageList(ListView):
    
    template_name = "packages/list.html"
    queryset = Package.objects.all().order_by("name")
    context_object_name = "packages"


class PackageDetail(DetailView):
    
    template_name = "packages/detail.html"
    model = Package
    context_object_name = "package"


class CommitsView(TemplateView):
    
    template_name = "packages/commits.html"
    
    def get_context_data(self, **kwargs):
        context = super(CommitsView, self).get_context_data(**kwargs)
        context["commits"] = Commit.active_commits()
        return context


class PullRequestList(ListView):
    
    template_name = "packages/pull_requests.html"
    queryset = PullRequest.objects.filter(
        state=PullRequest.STATE_OPEN
    ).order_by("created_at")
    context_object_name = "pull_requests"


def normalize(value, max_value):
    if value == 0 or max_value == 0:
        return 0
    return int(round(25 * log(value) / log(max_value)))


class DashboardView(TemplateView):
    
    template_name = "packages/dashboard.html"
    
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        
        six_months = [
            datetime.datetime(year=x[0], month=x[1], day=1)
            for x in final_months(6)
        ]
        
        context["months"] = six_months
        
        context["author_commits"] = CommitsByAuthorByMonth.objects.filter(
            month__gte=six_months[0]
        ).order_by("author__name", "-month")
        context["package_commits"] = CommitsByPackageByMonth.objects.filter(
            month__gte=six_months[0]
        ).order_by("package__name", "-month")
        
        return context
