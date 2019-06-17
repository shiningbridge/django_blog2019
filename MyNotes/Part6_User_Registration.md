## 第六部分 User Registration

建立另一个APP

第一步： 建立新APP，叫它users，并**更新**settings.py
`$ python manage.py startapp users`

in settings.py:
```python
# Application definition

INSTALLED_APPS = [
    'blog.apps.BlogConfig',     ## 每次加入新APP这里要更新一下的。。。结构是<APP>.apps.<CLASS>
    'user.apps.UsersConfig',    ## 其实，结构就是，model（class） 的路径。在user文件夹下apps.py里的UsersConfig类。
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


