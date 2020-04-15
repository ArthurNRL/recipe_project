from django.shortcuts import render
from .models import Post


# Create your views here.




def home(request):
    context = {
        'posts': Post.objects.all
    }
    return render(request, 'recipeSite/home.html', context, )


def about(request):
    return render(request, 'recipeSite/about.html', {'title': 'About'})
