from django.contrib import admin

from downloads.models import Release, ReleaseFile



class ReleaseFileInline(admin.StackedInline):
    model = ReleaseFile


class ReleaseAdmin(admin.ModelAdmin):
    list_display = ["version", "timestamp", "stable"]
    inlines = [
        ReleaseFileInline,
    ]



admin.site.register(Release, ReleaseAdmin)