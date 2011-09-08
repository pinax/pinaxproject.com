from math import log

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from packages.models import Package, Commit, PullRequest


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
    
    def get_img_url(self, commits, label="author"):
        url = "https://chart.googleapis.com/chart?chs=470x400&cht=s&"
        months = "|".join([
            x["month"].strftime("%b") for x in commits[0]["commits"]
        ])
        obj = "|".join([x[label].name for x in commits])
        chxl = "chxl=0:||%s||1:||%s|&" % (months, obj)
        
        max_commits = max([
            max([x["count"] for x in d["commits"]])
            for d in commits
        ])
        
        url += chxl
        
        first = ["0"]
        second = ["0"]
        third = ["0"]
        for i, obj in enumerate(commits):
            for j, commit in enumerate(obj["commits"]):
                first.append(str(j))
                second.append(str(i))
                third.append(
                    str(
                        normalize(commit["count"], max_commits)
                    )
                )
        chd = "t:%s|%s|%s" % (",".join(first), ",".join(second), ",".join(third))
        
        url += "chd=%s&" % chd
        
        chds = "-1,6,-1,%s,0,17" % len(commits)
        chm = "o,333333,1,-1,25"
        chxt = "x,y"
        
        url += "chds=%s&chm=%s&chxt=%s&" % (chds, chm, chxt)
        url += "chf=bg,s,efefef"
        return url
    
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        commits = Commit.commit_counts_by_month_by_person()
        context["commits"] = commits
        context["punchcard_url"] = self.get_img_url(commits)
        more_commits = Commit.commit_counts_by_month_by_package()
        context["project_punchcard_url"] = self.get_img_url(more_commits, label="package")
        return context
