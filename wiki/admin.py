from django.contrib import admin
from wiki.models import Page, LinkGroup, Link
from reversion_compare.admin import CompareVersionAdmin


class PageAdmin(CompareVersionAdmin):
    pass

admin.site.register(Page, PageAdmin)
admin.site.register(LinkGroup)
admin.site.register(Link)
