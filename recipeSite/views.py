from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from .models import Post
from users.models import Profile
from .forms import postUpdateForm, postCreateForm


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
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        print('query')
        return Post.objects.filter(author=user).order_by('-datePosted')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context['profile'] = Profile.objects.get(user=user)
        return context


class postDetailView(DetailView):
    model = Post
    template_name = 'recipeSite/postDetail.html'


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
