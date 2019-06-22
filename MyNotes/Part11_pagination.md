## 第十一部分 Pagination分页

学习点：

* 继续用class based views，加入分页pagination

### 多建一个View放每个用户自己的post

views.py中加入：
```python
from django.shortcuts import render, get_object_or_404
...
class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'    # 如果不是默认值，我们必须explicitly指定。默认是这么命名的，`<app>/<model>_<viewtype>.html`
    context_object_name = 'posts'       # 一样，如果不是默认值，我们必须explicitly指定。
    # ordering = ['-date_posted']       ## 可以在get_query_set 返回时候order一下。
    paginate_by = 5                     # pagination 就是这么简单。

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))    ## 从链接request的kwargs里找出username。返回一个用户对象，或者404找不到。这个具体username这个kwargs在哪，要在urls.py里定义。。
        return Post.objects.filter(author=user).order_by('-date_posted')

```

* `get_object_or_404`是从`django.shortcuts`里导入的。
* 直接加入paginate_by就好了。。。 --> 这个和home 页面里做法一样。
* overwrite `get_queryset`方法。
  * 从链接request的kwargs里找出`username`。返回一个用户对象，或者404找不到。这个具体username这个kwargs在哪，要在urls.py里定义。。

#### urls.py里定义

import 了 UserPostListView以后。

```python
...
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
...
```

* 这里就把`username`作为参数了。而且类型规定为`str`.


#### 分页按钮
当然要让分页显示出来，还要在view里改一下下。
在页面最底部吧：
```html
    {% if is_paginated %}

      {% if page_obj.has_previous %}
        <a class="btn btn-outline-info mb-4", href="?page=1">First</a>
        <a class="btn btn-outline-info mb-4", href="?page={{ page_obj.previous_page_number }}">上一页</a>
      {% endif %}

      {% for num in page_obj.paginator.page_range %}
        {% if page_obj.number == num %}
          <a class="btn btn-info mb-4", href="?page={{ num }}">{{ num }}</a>
        {% elif num > page_obj.number|add:'-3' and num < page_obj.number|add:'3' %}
          <a class="btn btn-outline-info mb-4", href="?page={{ num }}">{{ num }}</a>
        {% endif %}
      {% endfor %}

      {% if page_obj.has_next %}
        <a class="btn btn-outline-info mb-4", href="?page={{ page_obj.next_page_number }}">下一页</a>
        <a class="btn btn-outline-info mb-4", href="?page={{ page_obj.paginator.num_pages }}">Last</a>
      {% endif %}

    {% endif %}
```

* pipe这种操作。。。很深。
  * `num > page_obj.number|add:'-3'`，为啥不直接`num > page_obj.number-3`
* 也就是判断一下。网上学的。
