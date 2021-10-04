from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, UpdateView

from apps.accounts.forms import UserLoginForm, UserRegistrationForm, UserModelForm
from apps.blogapp.models import Article


@login_required
def favourite_list(request):
    new = Article.objects.filter(favourites=request.user)
    return render(request, 'accounts/favourite_list.html', {'new': new})


@login_required
def favourite_add(request, slug):
    post = get_object_or_404(Article, slug=slug)
    if post.favourites.filter(id=request.user.id).count() > 0:
        post.favourites.remove(request.user)
    else:
        post.favourites.add(request.user)
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def login_view(request):
    form = UserLoginForm(request.POST or None)
    _next = request.GET.get('next')
    if form.is_valid():
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        login(request, user)
        _next = _next or reverse_lazy('blogapp:home')
        return redirect(_next)
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse_lazy('blogapp:home'))


def registration_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'accounts/register_done.html', {'new_user': new_user})
        return render(request, 'accounts/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {'form': form})


class ProfileDetail(DetailView):
    model = get_user_model()
    template_name = 'accounts/profile_detail.html'


class ProfileDelete(DeleteView):
    model = get_user_model()
    template_name = 'accounts/profile_delete.html'
    success_url = reverse_lazy('blogapp:home')


class ProfileUpdate(UpdateView):
    model = get_user_model()
    template_name = 'accounts/profile_update.html'
    form_class = UserModelForm

    def get_success_url(self):
        return reverse_lazy('accounts:pofile', kwargs={'pk': self.get_object().pk})


@login_required
def subscribers_list(request):
    new = get_user_model().objects.filter(subscribers=request.user)
    return render(request, 'accounts/sub_list.html', {'new': new})


# TODO : доделать
@login_required
def subscribers_add(request, pk):
    subscribers = get_object_or_404(get_user_model(), pk=pk)
    subscribers.subscribers.add(request.user)
    #User.
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
    # if get_user_model().objects.filter(id=request.user.id).count() > 0:
    #     subscribers.remove(request.user)
    # else:
    #     subscribers.add(request.user)
    # return HttpResponseRedirect(request.META['HTTP_REFERER'])
