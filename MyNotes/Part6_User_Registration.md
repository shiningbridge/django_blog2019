## 第六部分 User Registration

建立另一个APP

### 第一步： 建立新APP，叫它users，并**更新**settings.py
`$ python manage.py startapp users`

in settings.py:
```python
# Application definition

INSTALLED_APPS = [
    'blog.apps.BlogConfig',     ## 每次加入新APP这里要更新一下的。。。结构是<APP>.apps.<CLASS>
    'users.apps.UsersConfig',   ## 其实，结构就是，model（class） 的路径。在users文件夹下apps.py里的UsersConfig类。
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

* views.py
加入form。。。和确认按钮，等。。

* urls.py
加入url链接。 可以从project的urls.py 入手改。。。
```python
"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from users import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('blog/', include('blog.urls')),    
    ## 先到project 目录的urls.py文件match 第一个url的route，剥离掉，进入下一层。
    ## 这里是指向了 ‘blog.urls’。。。
    ## 放空string，就是啥也不用填就直接redirect。
    path('', include('blog.urls')),    

]
```

### 前端的努力
```html
{% block content %}
    <div class="content-section">
        <!-- 用POST方法获取form的内容呀。 -->
        <form method="POST">
            {% csrf_token %}                <!-- csrf token 增加安全性用的。。。 -->
            <fieldset class="form-group">
                <legend class="border-bottom mb-4">Join Today</legend>
                <!-- {{ form.as_p }}      .as_p 可以让格式好看一点， as paragraph。。。 
                更进一步，可以用pipe ’|‘ 把crispy_form功能加进来-->
                {{ form | crispy }}
            </fieldset>
            <div class="form-group">
                <button class="btn btn-outline-info" type="submit">Sign Up</button>
            </div>
        </form>
        <div class="border-top pt-3">
            <small class="text-muted">
                Already Have An Account? <a class="ml-2" href="#">Sign In</a>
            </small>
        </div>
    </div>
{% endblock content %}
```


1. form格式
    - `.as_p` -- as paragraph


2. 用crispy_form美化。`pip install django-crispy-forms`
    - `| crispy` 把cripsy用起来。


base.html里加入alert功能。
```html
        <div class="col-md-8">
          {% if messages %}
            {% for message in messages %}
              <div class="alert alert-{{ message.tags }}">
                {{ message }}
              </div>
            {% endfor %}
          {% endif %}
          {% block content %}{% endblock %}
        </div>
```
在content顶上加入alert。
这个alert是通过messages传过来的。


### 后端

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()     ## 一步，就把user保存到数据库里了。
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created for {username}!')
            return redirect('blog-home')    ## 直接跳转。
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# messages.debug
# messages.info
# messages.success
# messages.warning
# messages.error
```
要让form起到作用，需要把内容传给后端。

1. 我们自己定制了UserRegisterForm，其实是继承了UserCreationForm. 下边细讲。
    - 可以接收`request.POST`，直接生成form object。
    - 让我们可以一步把form保存到数据库 `form.save()`
2. 我们用django提供的messages来内部发一些消息。
3. 我们还在成功注册后直接跳转，用到了`redirect()`作为返回值。

form.py: 我们自己的定制form
```python
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()  ## 定制其他field

    ## 这个是干嘛的呢？？？？
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```

继承了Django的UserCreationForm。
加入了email field。
[TODO] 不理解：
Meta类是干嘛的???
大概是告诉接收form object的模块，我有哪些field。依顺序都是什么。好把数据传进去。比如，写入数据库对应的列。
