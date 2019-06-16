## 第三部分 template

前两部分比较基础。会就会，不会就不会。。

这部分开始学新东西。。
In this Python Django Tutorial, we will be learning how to use templates to return more complex HTML to the browser. We'll also see how we can pass variables to our templates as context. Let's get started… 

The code for this series can be found at: https://github.com/CoreyMSchafer/code… 
Snippets: https://github.com/CoreyMSchafer/code...
Bootstrap Starter Template: https://getbootstrap.com/docs/4.0/get...


### 总结：
1. 建立templates文件夹，构建复杂HTML文件及目录结构。
2. HTML里的variables，templates，context，概念
    - 可以用code block里的分支，循环构建html
    -  {% if xxx %} ... {% endif %}
3. Bootstrap是什么东西。可以让网站layout瞬间高大上。
    - 直接用现成的JavaScript什么的。
4. URL集中管理
`href="/"` 改成 `href="{% url 'blog-home' %}"`
用code block。结合urlpatterns in urls.py


```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
]
```

### 解决的小问题：
1. <ExtendsNode: extends "blog/base.html"> must be the first tag in the template.
```html
{% extends "blog/base.html" %}  
<!--前边不能出现其他code block 例如{% comment %} {% endcomment %} 否则
<ExtendsNode: extends "blog/base.html"> must be the first tag in the template. -->

{% block content %}
    {% comment %} <h1>Blog home!</h1> {% endcomment %}
    {% for post in posts %}
        <h1>{{ post.title }}</h1>
        <p>By {{ post.author }} on {{ post.date_posted }}</p>
        <p>{{ post.content }}</p>
        
    {% endfor %}
{% endblock content %}
```




