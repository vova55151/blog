# Create your views here.
import statistics

import django_filters
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from django_filters import OrderingFilter
from django_filters.views import FilterView
from apps.accounts.forms import UserModelForm
from apps.blogapp.forms import *
from apps.blogapp.models import *
from apps.blogapp.task import send_email


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


class ArticleListView(FilterView):
    """
    Класс для отображения списка всех постов
    """
    model = Article
    paginate_by = 16
    template_name = 'blogapp/article_list.html'
    filterset_class = Filter


class ArticleDetailView(LoginRequiredMixin, MultipleObjectMixin, DetailView):
    """
    Класс для отображения информации о посте ,списком комментариев и формой для их отправки
    """
    model = Article
    template_name = 'blogapp/article_detail.html'
    paginate_by = 8

    def get_success_url(self):
        return reverse_lazy('blogapp:detail', kwargs={'slug': self.get_object().slug})

    def get_context_data(self, **kwargs):
        object_list = Comment.objects.filter(article=self.object, status='P')
        context = super().get_context_data(object_list=object_list, **kwargs)
        object = self.get_object()
        if self.request.user.is_authenticated:
            if get_user_model().objects.get(pk=object.author.pk).subscribers.filter(
                    pk=self.request.user.pk).exists():
                context["Sub"] = True
            else:
                context["Sub"] = False
            if object.favourites.filter(pk=self.request.user.pk).exists():
                context["Fav"] = True
            else:
                context["Fav"] = False
        context['recommended'] = Article.objects.filter(category=object.category).exclude(id=object.id)[0:5]
        context['comment_form'] = CommentModelForm()

        return context


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentModelForm
    template_name = 'blogapp/article_create.html'

    def get_object(self):
        return super().get_object(
            queryset=Article.objects.all()
        )

    def form_valid(self, form):
        comment_form = form.save(commit=False)
        comment_form.author = self.request.user
        comment_form.article = self.get_object()
        comment_form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('blogapp:detail', kwargs={'slug': self.get_object().slug})


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """
    Класс для создания поста
    """
    model = Article
    form_class = ArticleModelForm
    success_url = reverse_lazy('blogapp:home')
    template_name = 'blogapp/article_create.html'

    # c img inline
    def get(self, request, *args, **kwargs):
        """
        Обрабатывает запросы GET
        Возвращает пустую форму и ее встроенные наборы форм.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        img_inline = Img_inline()

        return self.render_to_response(
            self.get_context_data(form=form,
                                  img_inline=img_inline, ))

    def post(self, request, *args, **kwargs):
        """
        Обрабатывает запросы POST, создавая экземпляр формы и его встроенные наборы форм с переданными переменными POST
         Возвращает методы валидации формы
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        img_inline = Img_inline(self.request.POST, self.request.FILES, instance=form.instance)
        if form.is_valid() and img_inline.is_valid():

            return self.form_valid(form, img_inline)
        else:
            return self.form_invalid(form, img_inline)

    def form_valid(self, form, img_inline):
        """
        Присваивает посту автора и рассылает имейлы его подписчикам
        """

        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object = form.save()
        for i in img_inline:
            if i.cleaned_data:
                i.save()
        send_email(self.object.author.subscribers.all(), self.object.author, self.get_success_url())

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, img_inline):
        return self.render_to_response(self.get_context_data(form=form, img_inline=img_inline))

    def get_success_url(self):
        return reverse_lazy('blogapp:detail', kwargs={'slug': self.object.slug})


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    """
    Класс для редактирования поста
    """
    model = Article
    form_class = ArticleModelForm
    template_name = 'blogapp/article_update.html'

    def get_success_url(self):
        return reverse_lazy('blogapp:update', kwargs={'slug': self.get_object().slug})


class UserArticleList(LoginRequiredMixin, ListView):
    """
    Личный кабинет с формой смены пароля,данных пользователя и списка его статей
    """
    model = Article
    paginate_by = 10
    template_name = 'blogapp/article_user_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['pass_change'] = PasswordChangeForm(self.request.user)
        context['user_form'] = UserModelForm(instance=self.request.user)

        return context

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class PasswordView(PasswordChangeView):
    """
    Класс для редактирования пароля
    """
    form_class = PasswordChangeForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'blogapp/article_update.html'

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return redirect(reverse_lazy('accounts:profile'))


class UserUpdateView(UpdateView):
    """
    Класс для редактирования поста
    """
    model = get_user_model()
    form_class = UserModelForm
    success_url = reverse_lazy('accounts:profile')
    template_name = 'blogapp/article_update.html'

    def get_object(self):
        return self.request.user

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, form.errors)
        return redirect(reverse_lazy('accounts:profile'))


class ArticleDeleteView(DeleteView):
    """
    Класс для удаления поста
    """
    model = Article
    success_url = reverse_lazy('blogapp:home')
    template_name = 'blogapp/article_delete.html'
