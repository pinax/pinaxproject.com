from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from packages.models import Package


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
