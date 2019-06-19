## 第八部分 user profile and picture

学习点：
* 理解 Model 的作用。Profile model里加入picture功能
    - MVC里， model是数据存储，改变发生的地方。
* signal 很有用。怎么有用了。

### 添加内容 models 和 admin in users APP
model.py里：
```python
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)     # user is associated with this profile
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'
```

* OneToOneField方法，可以把两个不同的model关联起来。`on_delete=models.CASCADE`更是可以在一个instance被删后自动清除另一个。注意：是单向的。
* Model里很多属性都叫做`Field`。

admin.py里：需要register。这样才能用我们自定义的Profile模型。
```python
from django.contrib import admin
from .models import Profile

# Register your models here.
admin.site.register(Profile)
```
* 这里注意，其实不同APP里都会有admin.py。而且可以同时对admin页面起作用。
* [TODO] 先后顺序呢？？？


### picture的路径
* Django shell 看看user.profile.image
* profile.html template里，把image，username什么的加进去。


官方文档： 关于static 文件摆放
#### Serving files uploaded by a user during development¶
During development, you can serve user-uploaded media files from MEDIA_ROOT using the django.views.static.serve() view.

This is not suitable for production use! For some common deployment strategies, see Deploying static files.

For example, if your MEDIA_URL is defined as /media/, you can do this by adding the following snippet to your urls.py:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
我们自己加，并且加入判断，让代码更清晰。。
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```


### signaling怎么理解

```python
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

## 我们想自动给新注册用户创建profile
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
```
#### 具体解释：
**sender(`User`) do action/signaling `post_save` to the receiver which is the `create_profile` function..
This function take the signal and do the job.**

还有app.py要加点。。。
```python
from django.apps import AppConfig

class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        import users.signals
```
* `import users.signals` 说是官网推荐放在这个位置。
* [TODO]为什么要加入这个`ready`呢？？？
