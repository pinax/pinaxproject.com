import datetime

from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from packages.models import Package, Commit, PullRequest, final_months
from packages.models import CommitsByPackageByMonth, CommitsByAuthorByMonth


class AppList(ListView):
    
    template_name = "packages/list.html"
    queryset = Package.apps().order_by("name").select_related()
    context_object_name = "packages"


class StarterProjectList(ListView):
    
    template_name = "packages/list.html"
    queryset = Package.starter_projects().order_by("name").select_related()
    context_object_name = "packages"


class ThemeList(ListView):
    
    template_name = "packages/list.html"
    queryset = Package.themes().order_by("name").select_related()
    context_object_name = "packages"


class PackageList(ListView):
    
    template_name = "packages/list.html"
    queryset = Package.objects.all().order_by("name").select_related()
    context_object_name = "packages"


class PackageDetail(DetailView):
    
    template_name = "packages/detail.html"
    model = Package
    context_object_name = "package"


class CommitsView(TemplateView):
    
    template_name = "packages/commits.html"
    
    def get_context_data(self, **kwargs):
        context = super(CommitsView, self).get_context_data(**kwargs)
        context["commits"] = Commit.objects.filter(
            branch__active=True
        ).order_by("-committed_date").select_related()[:25]
        return context


class PullRequestList(ListView):
    
    template_name = "packages/pull_requests.html"
    queryset = PullRequest.objects.filter(
        state=PullRequest.STATE_OPEN
    ).order_by("created_at").select_related()
    context_object_name = "pull_requests"


class DashboardView(TemplateView):
    
    template_name = "packages/dashboard.html"
    
    def punchcard_url(self, commits, months):
        commits.sort()  # List of (total_count, name, month, commit_count)
        
        name_labels = []
        for commit in commits:
            if commit[1] not in name_labels:
                name_labels.append(commit[1])
        
        url = "https://chart.googleapis.com/chart"
        url += "?chs=550x%s&cht=s&" % (30 * len(name_labels))
        m = "|".join([x.strftime("%b") for x in months])
        obj = "|".join([
            y.name for y in name_labels
        ])
        chxl = "chxl=0:||%s||1:||%s|&" % (m, obj)
        
        url += chxl
        
        chd = "t:%s|%s|%s" % (
            ",".join([str(x) for x in range(len(months))] * (len(name_labels))),
            ",".join([",".join([str(x)] * len(months)) for x in range(len(name_labels))]),
            ",".join([str(x[3]) for x in commits])
        )
        
        url += "chd=%s&" % chd
        
        chds = "-1,%s,-1,%s,0,17" % (len(months), len(name_labels))
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
                author_commits[commit.author] = []
            author_commits[commit.author].append({
                "month": commit.month,
                "count": commit.commit_count
            })
        
        for author in author_commits.keys():
            summation = sum([x["count"] for x in author_commits[author]])
            if summation == 0:
                author_commits.pop(author) # don't show inactives
            else:
                for i, c in enumerate(author_commits[author]):
                    author_commits[author][i]["total_count"] = summation
        
        authors = []
        for author, value in author_commits.iteritems():
            for i, v in enumerate(value):
                authors.append(
                    (value[i]["total_count"], author, value[i]["month"], value[i]["count"])
                )
        
        package_commits_qs = CommitsByPackageByMonth.objects.filter(
            month__gte=six_months[0]
        ).order_by("package__pk", "-month").select_related()
        
        package_commits = {}
        for commit in package_commits_qs.all():
            if package_commits.get(commit.package) is None:
                package_commits[commit.package] = []
            package_commits[commit.package].append({
                "month": commit.month,
                "count": commit.commit_count
            })
        for package in package_commits.keys():
            summation = sum([x["count"] for x in package_commits[package]])
            if summation == 0:
                package_commits.pop(package) # don't show inactives
            else:
                for i, c in enumerate(package_commits[package]):
                    package_commits[package][i]["total_count"] = summation
        
        packages = []
        for package, value in package_commits.iteritems():
            for i, c in enumerate(package_commits[package]):
                packages.append(
                  (value[i]["total_count"], package, value[i]["month"], value[i]["count"])
                )
        
        context["author_punchcard_url"] = self.punchcard_url(authors, six_months)
        context["package_punchcard_url"] = self.punchcard_url(packages, six_months)
        
        return context
