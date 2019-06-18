## 第七部分 Login 和 Logout

### 建立page: login logout
urls.py里加login、logout页面
```python
    path('register/', user_views.register, name='注册'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LoginView.as_view(template_name='users/logout.html'), name='logout'),
```

urls.py 里有的url，会默认去找template。这些是Django管理的。 
如果这里没有，那就是野page了。

#### 理解path()

1. url相对地址。-- 叫做`route`
2. ~~用哪个view，用什么方法处理这个template。比如：用`auth_views.LoginView`里的as_view方法把template`users/login.html`处理成想要的page模样。~~
3. 给个名字，可以在template里的code block引用。比如： `{% url 'login' %}`

官方文档：

**path(route, view, kwargs=None, name=None)**

Returns an element for inclusion in `urlpatterns`.

The `view` argument is a view function or the result of `as_view()` for class-based views. It can also be an `django.urls.include()`.

views.py
```python
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()     ## 一步，就把user保存到数据库里了。
            username = form.cleaned_data.get('username')
            messages.success(request,f'Account created, ready for log in!')
            return redirect('login')    ## 直接跳转。
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required ## decoration,加入条件
def profile(request):
    return render(request, 'users/profile.html')
```
每个function专管render一个page。用什么context，用不用context，要function内部决定。

1. register就需要form。这个form从页面request里边提取。

    - 刚进入页面，没有POST（没填表呢还）：form是空的。
    - 填完表，用具有`type='submit'`的按钮POST一个request出来，这时候form就代了POST内容了。
        - 检查无误，可以操作写入数据库，跳转（redirect跳了，就不用render本页了）。
        - 有误则，根据错误重新render，提示修正。

2. profile这里就没有context。很简单。
    - 用到了decorator。进行条件判断。

login.html:
```html
Need An Account? <a class="ml-2" href="{% url '注册' %}">Sign Up Now</a>
```
注意：
1. `{% url '注册' %}`这个code block，直接从urls.py里解析出链接。可以用中文。 
2. login.html 和 register.html 文件基本没区别。
    - **这美极了**。这才叫template。
    - 两个页面的view其实不太一样。但都是根据context，render了一个page。这里context应该都是`{'form': form}`


in settings.py:
```python
# login redirect
LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'login'
```

加入一些默认跳转。这些页面不跳转的话，也可以工作，只不过不一定是我们想去的地方。就跟我们想用子类，而不是父类。


### 完善navigation bar关于user的部分

users/views.py
```python
from django.contrib.auth.decorators import login_required
...
...
@login_required
def profile(request):
    return render(request, 'users/profile.html')
```
加入register以外的，profile view。
其实就是根据`request`结果render一个html template -- `'users/profile.html'`，传入默认的context=NONE,这个以后看需要加。

#### base.html页面跟着改变
base.html
```html
            <div class="navbar-nav">
              {% if user.is_authenticated %}
                <a class="nav-item nav-link" href="{% url 'profile' %}">Profile</a>
                <a class="nav-item nav-link" href="{% url 'logout' %}">Logout</a>
              {% else %}
                <a class="nav-item nav-link" href="{% url 'login' %}">Login</a>
                <a class="nav-item nav-link" href="{% url '注册' %}">Register</a>
              {% endif %}
            </div>
```
用到条件句。

