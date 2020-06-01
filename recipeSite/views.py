from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView, View, FormView
from django.views.generic.edit import SingleObjectMixin
from .models import Post
from users.models import Profile, Favorites
from django.urls import reverse
from .forms import postUpdateForm, postCreateForm, favoriteForm


class postListView(ListView):
    model = Post
    template_name = 'recipeSite/home.html'
    context_object_name = 'posts'
    ordering = ['-datePosted']
    paginate_by = 20

class userListView(ListView):
    model = Post
    template_name = 'users/userPosts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=self.user).order_by('-datePosted')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['profile'] = Profile.objects.get(user=self.user)
        return context

class userFavoritesListView(ListView):
    model = Post
    template_name = 'users/userPosts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        self.user = get_object_or_404(User, username=self.request.user)
        favorites = Favorites.objects.filter(user=self.user)
        return Post.objects.filter(id=favorites.post)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.user)
        return context

class postDetail(View):
    def get(self, request, *args, **kwargs):
        view = postDetailView.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = postFavorited.as_view()
        return view(request, *args, **kwargs)

class postDetailView(DetailView):
    model = Post
    template_name = 'recipeSite/postDetail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = favoriteForm()
        context['favorite'] = False
        if(self.request.user.is_authenticated):
            self.profile = Profile.objects.get(user=self.request.user)
            if (self.profile in self.object.profile_set.all()):
                context['favorite'] = True
        return context

class postFavorited(LoginRequiredMixin ,DetailView):
    model = Post
    template_name = 'recipeSite/postDetail.html'

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('signin'))
        self.object = self.get_object()
        self.profile = Profile.objects.get(user=self.request.user)
        if (self.profile in self.object.profile_set.all()):
            self.profile.favoritePosts.remove(self.object)
        else:
            self.profile.favoritePosts.add(self.object)
        return HttpResponseRedirect(reverse('postDetail', kwargs={'pk': self.object.id}))

class postCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = postCreateForm
    template_name = 'recipeSite/post_form.html'
    extra_context = {'title': 'post'}

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class postUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = postCreateForm
    extra_context = {'title': 'Editar Postagem'}

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class postDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'recipeSite/about.html', {'title': 'About'})
