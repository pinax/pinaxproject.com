from django.contrib import admin

from downloads.models import Release, ReleaseFile



class ReleaseFileInline(admin.StackedInline):
    model = ReleaseFile


class ReleaseAdmin(admin.ModelAdmin):
    inlines = [
        ReleaseFileInline,
    ]



admin.site.register(Release, ReleaseAdmin)