from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

# Register your models here.
from apps.menu.models import Menu, TextPage


@admin.register(Menu)
class MenuAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_filter = ('pos', 'show')
    search_fields = ('name',)


@admin.action(description='Mark selected page as published')
def make_published(modeladmin, request, queryset):
    queryset.update(status=True)


@admin.action(description='Mark selected page as draft')
def make_dreaft(modeladmin, request, queryset):
    queryset.update(status=False)


@admin.register(TextPage)
class TextPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'date_created']
    actions = [make_published, make_dreaft]
