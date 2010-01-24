from django.contrib import admin

from example_sites.models import Site



class SiteAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "approved", "featured", "contact_name"]


admin.site.register(Site, SiteAdmin)