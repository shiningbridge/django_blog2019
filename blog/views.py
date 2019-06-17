from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post


def home(request):
    context = {
        'posts': Post.objects.all()     ## 用database拉。
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'} )   ## 从templates里找page。。。html
