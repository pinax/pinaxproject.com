import datetime

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


class DashboardView(TemplateView):
    
    template_name = "packages/dashboard.html"
    
    def punchcard_url(self, commits, months):
        url = "https://chart.googleapis.com/chart?chs=550x%s&cht=s&" % (30 * len(commits))
        m = "|".join([x.strftime("%b") for x in months])
        obj = "|".join([
            x.name for x,y in commits.iteritems()
        ])
        chxl = "chxl=0:||%s||1:||%s|&" % (m, obj)
        
        url += chxl
        
        first = ["0"]
        second = ["0"]
        third = ["0"]
        for i, key in enumerate(commits):
            for j, commit in enumerate(commits[key]["commits"]):
                first.append(str(j))
                second.append(str(i))
                third.append(str(commit["count"]))
        chd = "t:%s|%s|%s" % (",".join(first), ",".join(second), ",".join(third))
        
        url += "chd=%s&" % chd
        
        chds = "-1,%s,-1,%s,0,17" % (len(months), len(commits))
        chm = "o,333333,1,-1,22"
        chxt = "x,y"
        
        url += "chds=%s&chm=%s&chxt=%s&" % (chds, chm, chxt)
        url += "chf=bg,s,efefef"
        return url
    
    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        
        six_months = [
            datetime.datetime(year=x[0], month=x[1], day=1)
            for x in final_months(6)
        ]
        
        six_months.reverse()
        
        context["months"] = six_months
        
        author_commits_qs = CommitsByAuthorByMonth.objects.filter(
            month__gte=six_months[0]
        ).order_by("author__pk", "month").select_related()

        author_commits = {}
        for commit in author_commits_qs.all():
            if author_commits.get(commit.author) is None:
                author_commits[commit.author] = {"commits": []}
            author_commits[commit.author]["commits"].append({
                "month": commit.month,
                "count": commit.commit_count
            })
        for author in author_commits.keys():
            if sum([x["count"] for x in author_commits[author]["commits"]]) == 0:
                author_commits.pop(author) # don't show inactives
        
        package_commits_qs = CommitsByPackageByMonth.objects.filter(
            month__gte=six_months[0]
        ).order_by("package__name", "-month").select_related()
        
        package_commits = {}
        for commit in package_commits_qs.all():
            if package_commits.get(commit.package) is None:
                package_commits[commit.package] = {"commits": []}
            package_commits[commit.package]["commits"].append({
                "month": commit.month,
                "count": commit.commit_count
            })
        for package in package_commits.keys():
            if sum([x["count"] for x in package_commits[package]["commits"]]) == 0:
                package_commits.pop(package) # don't show inactives
        
        context["author_commits"] = author_commits
        context["package_commits"] = package_commits
        
        context["author_punchcard_url"] = self.punchcard_url(author_commits, six_months)
        context["package_punchcard_url"] = self.punchcard_url(package_commits, six_months)
        
        return context
