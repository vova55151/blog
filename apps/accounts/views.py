from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, DeleteView, UpdateView, TemplateView, ListView
from django_registration.backends.activation.views import RegistrationView, ActivationView

from apps.accounts.forms import UserForm
from apps.blogapp.models import Article

# @login_required
# def favourite_list(request):
#     new = Article.objects.filter(favourites=request.user)
#     return render(request, 'accounts/favourite_list.html', {'new': new})
#
#
# @login_required
# def favourite_add(request, slug):
#     post = get_object_or_404(Article, slug=slug)
#     if post.favourites.filter(id=request.user.id).count() > 0:
#         post.favourites.remove(request.user)
#         post.likes_count -= 1
#     else:
#         post.likes_count += 1
#         post.favourites.add(request.user)
#     post.save()
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])


class FavouritesAddView(LoginRequiredMixin, View):
    """
    добавляет в избренное статью,если в избранном - удаляет
    """

    def get(self, request, **kwargs):
        post = get_object_or_404(Article, slug=kwargs['slug'])
        if post.favourites.filter(id=request.user.id).exists():
            post.favourites.remove(self.request.user)
        else:
            post.favourites.add(self.request.user)
        post.likes_count = post.favourites.count()
        post.save()
        return HttpResponseRedirect(reverse_lazy('blogapp:detail', kwargs={'slug': post.slug}))


#
# def login_view(request):
#     form = UserLoginForm(request.POST or None)
#     _next = request.GET.get('next')
#     if form.is_valid():
#         email = form.cleaned_data.get('email')
#         password = form.cleaned_data.get('password')
#         user = authenticate(email=email, password=password)
#         login(request, user)
#         _next = _next or reverse_lazy('blogapp:home')
#         return redirect(_next)
#     return render(request, 'accounts/login.html', {'form': form})
#
#
# def logout_view(request):
#     logout(request)
#     return redirect(reverse_lazy('blogapp:home'))
#

# def registration_view(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(request.POST)
#         if form.is_valid():
#             new_user = form.save(commit=False)
#             new_user.set_password(form.cleaned_data['password'])
#             new_user.save()
#             return render(request, 'accounts/register_done.html', {'new_user': new_user})
#         return render(request, 'accounts/registration_form.html', {'form': form})
#     else:
#         form = UserRegistrationForm()
#         return render(request, 'accounts/registration_form.html', {'form': form})


class UserLoginView(LoginView):
    # authentication_form = UserLoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):

    def get_next_page(self):
        return reverse_lazy('blogapp:home')


# class ProfileDetail(DetailView, LoginRequiredMixin):
#     model = get_user_model()
#     template_name = 'accounts/profile_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if get_user_model().objects.filter(subscribers=self.request.user).exists():
#             context["Sub"] = True
#         else:
#             context["Sub"] = False
#         return context


class ProfileDelete(LoginRequiredMixin, DeleteView):
    """
    Удаление профиля
    """
    model = get_user_model()
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('blogapp:home')


# class ProfileUpdate(UpdateView):
#     model = get_user_model()
#     template_name = 'accounts/profile_update.html'
#     form_class = UserModelForm
#
#     def get_success_url(self):
#         return reverse_lazy('accounts:profile', kwargs={'pk': self.get_object().pk})


# @login_required
# def subscribers_list(request):
#     return render(request, 'accounts/sub_list.html', {'new': new})
#
#
# @login_required
# def subscribers_add(request, pk):
#     user = get_object_or_404(get_user_model(), pk=pk)
#     if user.subscribers.filter(pk=request.user.pk).exists():
#         request.user.subscribers.remove(user)
#     else:
#         request.user.subscribers.add(user)
#     return HttpResponseRedirect(request.META['HTTP_REFERER'])


class SubList(LoginRequiredMixin, ListView):
    """
    Список подписчиков
    """
    model = get_user_model()
    template_name = 'accounts/sub_list.html'
    paginate_by = 10

    def get_queryset(self):
        return get_user_model().objects.filter(subscribers=self.request.user)


class FavList(LoginRequiredMixin, ListView):
    """
    список избранного
    """
    model = Article
    template_name = 'accounts/favourite_list.html'
    paginate_by = 10

    def get_queryset(self):
        return Article.objects.filter(favourites=self.request.user)


class UserRegistrationView(RegistrationView):
    """
    регистрация с отправкой письма на почту
    """
    template_name = 'accounts/registration_form.html'
    form_class = UserForm
    email_body_template = 'accounts/activation_email_body.txt'
    email_subject_template = 'accounts/activation_email_subject.txt'
    success_url = reverse_lazy('success_registration')


class SuccessRegistrationView(TemplateView):
    """
    Успешная регистрация
    """
    template_name = 'accounts/success_registration.html'


class SubscribersAdd(LoginRequiredMixin, View):
    """
    Подписывает пользователя на автора статьи,если подписан - отписывает
    """

    def get(self, request, **kwargs):
        print()
        author = get_user_model().objects.get(pk=kwargs['pk'])
        if self.request.user != author:
            if author.subscribers.filter(pk=self.request.user.pk).exists():
                author.subscribers.remove(self.request.user)
            else:
                author.subscribers.add(self.request.user)
            author.save()
        return HttpResponseRedirect(self.request.GET.get('next', f'{reverse_lazy("blogapp:home")}'))


class UserActivationView(ActivationView):
    """

    """
    success_url = reverse_lazy('blogapp:home')

    def activate(self, *args, **kwargs):
        username = self.validate_key(kwargs.get("activation_key"))
        user = self.get_user(username)
        user.is_active = True
        user.save()
        login(self.request, user)
        return user
