## 第十部分 Create, Update, and Delete Posts

学习点：
* 用class based views，实现Create, Update, and Delete Posts...

### 小总结：view.py 做什么？model？还有template?

* 是把同一个model （Post）筛选展示出不同效果，用于不同的用途。和用户交互的基本平台。
* model单纯做数据的结构，存储。
* template是view在浏览器上具体layout

### 比较class base views and function based views

* 好处多多呀。
* 简洁省力。

```python
from django.shortcuts import render
# from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
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

```

* 先不加入改密码的功能，这里改不安全。

* 善用class view。
  * 需要了解一些基本值，路径的默认寻找规则：
  * 比如：looking for template:`<app>/<model>_<viewtype>.html`

#### redirect vs. reverse

reverse是通过url name 找对应的url，返回url string。常和redirect一起用，用来给redirect找地址url。

#### 不让别人改你的post

* 需要加一个验证用户功能。
* 因为不能像function那样用decoration。Class如果要加入判断。 我们要用到`mixin` 这个功能。 
* 其实就是继承。叫做mixin，表示帮你加入些功能。像插件一样`plugin`。


#### Delete post

默认叫做post_confirm_delete.html 的template 是PostDeleteForm需要的一个Confirm页面。一旦Submit，check没有权限问题，就要delete了。
```html
{% extends "blog/base.html" %}
{% block content %}
    <div class="content-section">
        <!-- 用POST方法获取form的内容呀。 -->
        <form method="POST">
            {% csrf_token %}                <!-- csrf token 增加安全性用的。。。 -->
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Delete 条目</legend>
                <h2>Sure to delete the Post: "{{ object.title }}"</h2>
            </fieldset>
            <div class="form-group">
                <button class="btn btn-outline-danger" type="submit">Yes, Delete</button>
                <a class="btn btn-outline-secondary" href="{% url 'post-detail' object.id %}">Cancel</a>
            </div>
        </form>
    </div>
{% endblock content %}
```

#### 把这些操作的链接按钮，create， delete，update 放到view里边。

* create按钮放在nav-bar上。

* update， delete放在post_detail.html template里：

```html
          <div> 
            {% if object.author == user %}
              <a class="btn btn-secondary btn-sm mt-1 mb-1" href="{% url 'post-update' object.id %}">Update</a>
              <a class="btn btn-danger btn-sm mt-1 mb-1" href="{% url 'post-delete' object.id %}">Delete</a>
            {% endif %}
          </div>
```

第一层防护：自己的post才会出现按钮。
第二层防护：之前的判断是不是author。不是的话delete url会显示403 Forbidden。