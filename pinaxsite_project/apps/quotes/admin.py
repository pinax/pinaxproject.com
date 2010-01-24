from django.contrib import admin

from quotes.models import Quote



class QuoteAdmin(admin.ModelAdmin):
    list_display = ["id", "text", "added"]


admin.site.register(Quote, QuoteAdmin)