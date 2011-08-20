from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from packages.models import Package, PackageBranch


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
        context["commits"] = PackageBranch.active_branch_commits()
        return context
