from django.contrib import admin
from wiki.models import Page
from reversion_compare.admin import CompareVersionAdmin


class PageAdmin(CompareVersionAdmin):
    pass

admin.site.register(Page, PageAdmin)
