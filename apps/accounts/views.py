from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, UpdateView
from django_registration.backends.activation.views import RegistrationView

from apps.accounts.forms import UserLoginForm, UserRegistrationForm, UserModelForm
from apps.blogapp.models import Article


@login_required
def favourite_list(request):
    new = Article.objects.filter(favourites=request.user)
    return render(request, 'accounts/favourite_list.html', {'new': new})

#TODO : через Update View в post или form_valid добавить к кнопкам сердечко https://icons.getbootstrap.com/#install
@login_required
def favourite_add(request, slug):
    post = get_object_or_404(Article, slug=slug)
    if post.favourites.filter(id=request.user.id).count() > 0:
        post.favourites.remove(request.user)
        post.likes_count -= 1
    else:
        post.likes_count += 1
        post.favourites.add(request.user)
    post.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


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

def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
        return render(request, 'accounts/registration_form.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'accounts/registration_form.html', {'form': form})


# TODO : sendgreed

# class UserRegistrationView(RegistrationView):


class UserLoginView(LoginView):
    # authentication_form = UserLoginForm
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    def get_next_page(self):
        return self.request.GET.get('next', '/')


class ProfileDetail(DetailView):
    model = get_user_model()
    template_name = 'accounts/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if get_user_model().objects.filter(subscribers=self.request.user).exists():
            context["Sub"] = True
        else:
            context["Sub"] = False
        return context


class ProfileDelete(DeleteView):
    model = get_user_model()
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('blogapp:home')


class ProfileUpdate(UpdateView):
    model = get_user_model()
    template_name = 'accounts/profile_update.html'
    form_class = UserModelForm

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'pk': self.get_object().pk})


@login_required
def subscribers_list(request):
    new = get_user_model().objects.filter(subscribers=request.user)
    return render(request, 'accounts/sub_list.html', {'new': new})


@login_required
def subscribers_add(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if user.subscribers.filter(pk=request.user.pk).exists():
        request.user.subscribers.remove(user)
    else:
        request.user.subscribers.add(user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
