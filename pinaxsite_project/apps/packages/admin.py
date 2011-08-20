from django.contrib import admin

from packages.models import Package, PackageBranch



class PackageBranchInline(admin.StackedInline):
    model = PackageBranch


class PackageAdmin(admin.ModelAdmin):
    list_display = ["name", "package_type", "pinax_external"]
    inlines = [
        PackageBranchInline,
    ]



admin.site.register(Package, PackageAdmin)