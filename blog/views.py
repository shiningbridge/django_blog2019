from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

myposts = [
    {
        'author': '张三',
        'title': 'Blog post 1',
        'content': 'First post content',
        'date_posted': '2019-06-14'
    },
    {
        'author': '李四',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': '2019-06-14'
    },
]


def home(request):
    context = {
        'posts': myposts     ## the key 'posts'可以做html里的变量用'.' 语法调用
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'} )   ## 从templates里找page。。。html
