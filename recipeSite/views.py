from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse
from .models import Post, Ingredients
from .forms import postUpdateForm,postCreateForm


def home(request):
    context = {
        'posts': Post.objects.all
    }
    print(Ingredients.objects.all())
    return render(request, 'recipeSite/home.html', context, )

class postListView(ListView):
    model = Post
    template_name = 'recipeSite/home.html'
    context_object_name = 'posts'
    ordering = ['-datePosted']

class postDetailView(DetailView):
    model = Post
    template_name = 'recipeSite/postDetail.html'

class postCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = postCreateForm
    template_name = 'recipeSite/post_form.html'

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class postUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = postUpdateForm

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        # postUpdateForm.getFields(self.object)
        self.getFields()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        # self.getFields()
        return super().post(request, *args, **kwargs)



    def getFields(self):
        n = 1
        print('generate')
        # print(self.object.ingredientList())
        for ingredient in (self.object.ingredientList()):
            # postUpdateForm[ingredients{n}] = forms.CharField(required=False)
            # postUpdateForm.Meta.fields += [f'ingredients{n}']
        #     exec(f'self.initial[-1] = self.ingredient{n}')
        #     # self.fields += [f'ingredient{n}']
            n += 1






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
