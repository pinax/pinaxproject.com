from django.contrib import admin

from packages.models import Package, CommitActivityFeed



class CommitActivityFeedInline(admin.StackedInline):
    model = CommitActivityFeed


class PackageAdmin(admin.ModelAdmin):
    list_display = ["name", "package_type", "pinax_external"]
    inlines = [
        CommitActivityFeedInline,
    ]



admin.site.register(Package, PackageAdmin)