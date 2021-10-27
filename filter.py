import django_filters
from django_filters import OrderingFilter

from apps.blogapp.models import Category, Article


class Filter(django_filters.FilterSet):
    """
    Настройка фильтра под древовидную структуру категорий поста
    """

    def filter_by_category(self, queryset=None, value=None):
        category = value
        if category.get_descendants():
            queryset1 = self.filter(category__in=category.get_descendants())
            queryset2 = self.filter(category__exact=category)
            queryset = queryset1 | queryset2
        else:
            queryset = self.filter(category=category)
        return queryset

    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        method=filter_by_category
    )
    name = django_filters.CharFilter(lookup_expr='icontains')
    o = OrderingFilter(
        fields=(
            ('rating', 'rating'),
            ('author', 'author'),
            ('category', 'category'),
            ('date_created', 'date_created'),
        ),
    )

    class Meta:
        model = Article
        fields = ['author', 'category']