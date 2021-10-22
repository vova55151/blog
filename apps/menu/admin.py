from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

# Register your models here.
from apps.menu.models import Menu, TextPage

admin.site.register(TextPage)

@admin.register(Menu)
class MenuAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_filter = ('pos', 'show')
    search_fields = ('name',)

