from django.utils.translation import ugettext_lazy
from rest_framework import permissions


class ArticleAuthorAccessPermission(permissions.BasePermission):
    message = ugettext_lazy('Вы не являетесь автором статьи')

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
