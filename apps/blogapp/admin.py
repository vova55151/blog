# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from django.contrib.auth.models import Group

from apps.accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from apps.accounts.models import User
from apps.blogapp.models import Subcategory, Category, Article, Comment, Like, Image
from apps.menu.models import Menu


class GroupInstanceInline(admin.TabularInline):
    model = Group


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'img', 'user_permissions',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'password1', 'password2', 'is_staff', 'is_active', 'img', 'user_permissions',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    # inlines = [GroupInstanceInline]


admin.site.register(User, CustomUserAdmin)

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Menu)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Image)


# TODO : django admin sortable 2 pip install
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'author', 'category', 'subcategory', 'descr', 'content', 'rec', 'rating',
                    'comments_count', 'likes_count', 'date_created', 'date_edit')
    prepopulated_fields = {'slug': ('name',)}
