# Create your views here.
import statistics

import django_filters
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib import messages
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
        # tuple-mapping retains order
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


class ArticleDetailView(DetailView, CreateView):
    """
    Класс для отображения информации о посте ,списком комментариев и формой для их отправки
    """

    model = Article
    template_name = 'blogapp/article_detail.html'
    # TODO : сделать через 2 вьюхи ,передавая одну в шаблоне формы в action
    form_class = CommentModelForm

    def form_valid(self, form):
        comment_form = form.save(commit=False)
        comment_form.author = self.request.user

        comment_form.article = self.get_object()
        # object_list = Comment.objects.filter(article=self.object)
        # print(object_list)
        # if object_list:
        #     self.get_object().rating = statistics.mean([int(i.rating) for i in object_list])
        #

        comment_form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        object = self.get_object()
        comments = object.comment_set.filter(status="P")
        if self.request.POST:
            comment_form = self.form_class(self.request.POST)
        else:
            comment_form = CommentModelForm()
        author = get_user_model().objects.get(pk=self.get_object().author.pk)
        if self.request.user.is_authenticated:
            if author.subscribers.filter(pk=self.request.user.pk).exists():
                context["Sub"] = True
            else:
                context["Sub"] = False
            if self.get_object().favourites.filter(pk=self.request.user.pk).exists():
                context["Fav"] = True
            else:
                context["Fav"] = False
        context['recommended'] = Article.objects.filter(category=object.category).exclude(id=object.id)[0:5]
        context['comment_form'] = comment_form
        context['comments'] = comments

        return context

    # def get_context_data(self, **kwargs):
    #     # qs = Article.objects.prefetch_related('comment_set').filter(article_name=self.object)
    #     object_list = Comment.objects.filter(article=self.object, status='P')
    #     if object_list:
    #         rating = statistics.mean([i.comment_rating for i in object_list])
    #     else:
    #         rating = 0
    #
    #     context = super().get_context_data(object_list=object_list, **kwargs)
    #     context['rating'] = rating
    #     # context['form'] = CommentModelForm(initial={
    #     #     'article': self.object,
    #     #     'comment_name': f'{self.request.user.first_name} {self.request.user.last_name}',
    #     # })
    #     if self.request.POST:
    #         context['comment_form'] = self.form_class(self.request.POST)
    #     else:
    #         context['comment_form'] = CommentModelForm()
    #
    #     return context

    def get_success_url(self):
        return reverse_lazy('blogapp:detail', kwargs={'slug': self.get_object().slug})


# class CommentCreateView(CreateView):
#     model = Comment
#     form_class = CommentModelForm
#     success_url = reverse_lazy('blogapp:home')
#     template_name = 'article_create.html'


# def post_detail(request, slug):
#     article = get_object_or_404(Article, slug=slug)
#     # List of active comments for this post
#     comments = article.comment_set.filter(article=article)
#
#     if request.method == 'POST':
#         # A comment was posted
#         comment_form = CommentModelForm(data=request.POST)
#         if comment_form.is_valid():
#             # Create Comment object but don't save to database yet
#             new_comment = comment_form.save(commit=False)
#             # Assign the current post to the comment
#             new_comment.post = slug
#             # Save the comment to the database
#             new_comment.save()
#     else:
#         comment_form = CommentModelForm()
#     return render(request,
#                   'article_detail.html',
#                  {'article': article,
#                   'comments': comments,
#                   'comment_form': comment_form})


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
        # print(self.request.POST, self.request.FILES)
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
        for d in self.object.author.subscribers.all():
            d.email_user('subject', 'message', 'from_email@test.com')

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, img_inline):
        return self.render_to_response(self.get_context_data(form=form, img_inline=img_inline))

    # def form_valid(self, form):
    #     """
    #     Присваивает посту автора и рассылает имейлы его подписчикам
    #     """
    #
    #     self.object = form.save(commit=False)
    #     self.object.author = self.request.user
    #     self.object = form.save()
    #
    #     for d in self.object.author.subscribers.all():
    #         d.email_user('subject', 'message', 'from_email@test.com')
    #
    #     return HttpResponseRedirect(self.get_success_url())
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['form'] = ArticleModelForm(self.request.POST)
    #
    #     else:
    #         context['form'] = ArticleModelForm()
    #
    #     return context


# class ImgCreateView(CreateView):
#     """
#     Класс для создания проекта
#     """
#     model = Image
#     form_class = ImgModelForm
#     success_url = reverse_lazy('blogapp:home')
#     template_name = 'blogapp/img_create.html'


class ArticleUpdateView(UpdateView):
    """
    Класс для редактирования поста
    """
    model = Article
    form_class = ArticleModelForm
    template_name = 'blogapp/article_update.html'

    def get_success_url(self):
        return reverse_lazy('blogapp:update', kwargs={'slug': self.get_object().slug})


class UserArticleList(ListView, LoginRequiredMixin):
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
