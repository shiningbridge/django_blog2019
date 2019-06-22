from django.shortcuts import render, get_object_or_404
# from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    )
from blog.models import Post


def home(request):
    context = {
        'posts': Post.objects.all()     ## 用database拉。
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'    # 如果不是默认值，我们必须explicitly指定。默认是这么命名的，`<app>/<model>_<viewtype>.html`
    context_object_name = 'posts'       # 一样，如果不是默认值，我们必须explicitly指定。
    ordering = ['-date_posted']
    paginate_by = 5                     # pagination 就是这么简单。


class PostDetailView(DetailView):
    model = Post                        # 用了属性的默认命名规范，则不用单独制定了。对比PostListView。简单多了。


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        '''CreateView 强制查有没有author.没有就过不去。
        这里overwrite, set the author to current user.'''
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user    ## 这里也把当前用户填入的author栏，写入表格form。
        return super().form_valid(form)

    def test_func(self):            ## overwrite。让不让进行操作。
        post = self.get_object()    ## 从这个View找到object。为什么不叫instance？
        if self.request.user == post.author:
            return True
        return False


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'    # 如果不是默认值，我们必须explicitly指定。默认是这么命名的，`<app>/<model>_<viewtype>.html`
    context_object_name = 'posts'       # 一样，如果不是默认值，我们必须explicitly指定。
    # ordering = ['-date_posted']       ## 可以在get_query_set 返回时候order一下。
    paginate_by = 5                     # pagination 就是这么简单。

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'               ## delete成功后，跳转到。

    def test_func(self):            ## overwrite。让不让进行操作。
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'} )   ## 从templates里找page。。。html
