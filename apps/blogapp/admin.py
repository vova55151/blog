# Register your models here.

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register your models here.
from django.contrib.auth.models import Group
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory, MoveNodeForm

from apps.accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from apps.accounts.models import User
from apps.blogapp.models import  Category, Article, Comment, Image
from apps.menu.models import Menu


class GroupInstanceInline(admin.TabularInline):
    model = Group


class CategoryNodeForm(MoveNodeForm):
    class Meta:
        model = Category
        exclude = []


@admin.register(Category)
class CategoryAdmin(TreeAdmin):
    form = movenodeform_factory(Category, CategoryNodeForm)


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'subscribers')}),
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


class MenuNodeForm(MoveNodeForm):
    class Meta:
        model = Menu
        exclude = []


@admin.register(Menu)
class MenuAdmin(TreeAdmin):
    form = movenodeform_factory(Menu, MenuNodeForm)


admin.site.register(User, CustomUserAdmin)


admin.site.register(Comment)
admin.site.register(Image)


# TODO : django admin sortable 2 pip install
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'author', 'category', 'descr', 'content', 'rating',
                    'comments_count', 'likes_count', 'date_created', 'date_edit')
    prepopulated_fields = {'slug': ('name',)}
