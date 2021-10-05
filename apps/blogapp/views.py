# Create your views here.
import statistics

import django_filters
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from django.views.generic.list import MultipleObjectMixin
from django_filters import OrderingFilter
from django_filters.views import FilterView

from apps.blogapp.forms import *
from apps.blogapp.models import *


class Filter(django_filters.FilterSet):
    """
    Класс для корректной работы фильтра по ключевым словам
    """
    name = django_filters.CharFilter(lookup_expr='icontains')
    o = OrderingFilter(
        # tuple-mapping retains order
        fields=(
            ('rating', 'rating'),
            ('author', 'author'),
            ('category', 'category'),
            ('date_created', 'date_created'),
        ),

        # labels do not need to retain order
        # field_labels={
        #
        # }
    )

    class Meta:
        model = Article
        fields = ['author', 'category']


class ArticleListView(FilterView):
    """
    Класс для отображения списка всех проектов
    """
    model = Article
    paginate_by = 16
    template_name = 'blogapp/article_list.html'
    filterset_class = Filter


class ArticleDetailView(DetailView, CreateView):
    """
    Класс для отображения информации о проекте
    """

    model = Article
    template_name = 'blogapp/article_detail.html'
    # success_url = reverse_lazy('blogapp:home')  # TODO : сделать через 2 вьюхи ,передавая одну в шаблоне формы в
    #  action
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
        comments = object.comment_set.all()
        if self.request.POST:
            comment_form = self.form_class(self.request.POST)
        else:
            comment_form = CommentModelForm()
        context['recommended'] = Article.objects.filter(category=self.get_object().category).exclude(id=object.id)
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


class ArticleCreateView(CreateView):
    """
    Класс для создания проекта
    """
    model = Article
    form_class = ArticleModelForm
    success_url = reverse_lazy('blogapp:home')
    template_name = 'blogapp/article_create.html'

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
        Вызывается, если все формы валидны. Создает экземпляр телефона ,контактных лиц и Email
        Возвращает редирект на страницу списка компаний
        """
        # img_inline.instance = self.object
        # img_inline.save()
        # self.request.FILES['img']
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object = form.save()
        for i in img_inline:
            if i.cleaned_data:
                i.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, img_inline):
        return self.render_to_response(self.get_context_data(form=form, img_inline=img_inline))

    # def form_valid(self, form,img_inline):
    #     """
    #     Вызывается, если все формы валидны. Создает экземпляр телефона ,контактных лиц и Email
    #     Возвращает редирект на страницу списка компаний
    #     """
    #     context = self.get_context_data()
    #     article_form = form.save(commit=False)
    #     article_form.author = self.request.user
    #     article_form.save()
    #     img_inline.save()
    #     # context['img_inline'].instance = self.object
    #     # context['img_inline'].instance.save()
    #     return super().form_valid(form,img_inline)

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     if self.request.POST:
    #         context['form'] = ArticleModelForm(self.request.POST)
    #         context['img_inline'] = Img_inline(self.request.POST)
    #     else:
    #         context['form'] = ArticleModelForm()
    #         context['img_inline'] = Img_inline()
    #     return context


class ImgCreateView(CreateView):
    """
    Класс для создания проекта
    """
    model = Image
    form_class = ImgModelForm
    success_url = reverse_lazy('blogapp:home')
    template_name = 'blogapp/img_create.html'


class ArticleUpdateView(UpdateView):
    """
    Класс для редактирования проекта
    """
    model = Article
    form_class = ArticleModelForm
    success_url = reverse_lazy('blogapp:home')
    template_name = 'blogapp/article_update.html'


class ArticleDeleteView(DeleteView):
    """
    Класс для удаления проекта
    """
    model = Article
    success_url = reverse_lazy('blogapp:home')
    template_name = 'blogapp/article_delete.html'
