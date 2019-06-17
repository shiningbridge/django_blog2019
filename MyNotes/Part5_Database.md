## 第五部分 Database and Migration

ORM (object relational mapper)
用同样的代码管理不同的数据库。。。。

### MVC 模型
models 用class实现。写在 models.py 文件里。

* user model 可以改。
* post model 自己写。

给代码，加入model。 其实是用class实现的。

```python
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)  ## timezone.now后边不加括号()，因为不想让他执行，只是引用
    ## auto_now=True老是变... auto_now_add=True完全不变
    author = models.ForeignKey(User, on_delete = models.CASCADE)
```

### 理解 migration


makemigration后，上边的model生成了这个migrations/0001_initial.py 文件

```python
# Generated by Django 2.2.1 on 2019-06-16 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
```

#### 如何理解migration
* makemigration：对应编译 （make），把抽象上层model，针对选择的不同底层数据库，编译成可以操作不同底层SQL数据库的代码。
* migrate：对应运行。

默认目前用的数据库是 SQLite. 命令`python manage.py sqlmigrate blog 0001`就相当于运行这个0001_inital.py 文件的结果。
打印出具体建立了什么table。什么属性。。。

**注意： 这一切，我们都不用知道。migration帮我们搞定啦。。。**

```SQL
 (django_env)   python manage.py sqlmigrate blog 0001
BEGIN;
--
-- Create model Post
--
CREATE TABLE "blog_post" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "content" text NOT NULL, "date_posted" datetime NOT NULL, "author_id" integer NOT NULL REFERENCES "auth_user" ("id") DEFERRABLE INITIALLY DEFERRED);
CREATE INDEX "blog_post_author_id_dd7a8485" ON "blog_post" ("author_id");
COMMIT;
```

```shell
 (django_env)   python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, blog, contenttypes, sessions
Running migrations:
  Applying blog.0001_initial... OK
```

### python shell 验证 ORM (很好的练习)
一旦migrate了。 就可以开一个shell，验证一下。。
```python
 (django_env)   python manage.py shell   
Python 3.7.3 (default, Mar 27 2019, 16:54:48)
[Clang 4.0.1 (tags/RELEASE_401/final)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>>
>>> from blog.models import Post
>>> from django.contrib.auth.models import User
>>> User.objects
<django.contrib.auth.models.UserManager object at 0x1078ca160>
>>> User.objects.all()
<QuerySet [<User: ShiningBridge>, <User: TestUser>]>
>>> user = User.objects.filter(username='ShiningBridge').first()
>>> user
<User: ShiningBridge>
>>> User.objects.filter(username='ShiningBridge').first().id
1
>>> user.id
1
>>> user.pk
1
>>>
```
pk --> primary key
默认是指向id的。所以也是1。

继续：
```python
>>> Post.objects.all()
<QuerySet []>
>>> post_1 = Post(title='Blog 1', content='First Post 内容', author=user)
>>> Post.objects.all()
<QuerySet []>
>>> Post.objects.all()
<QuerySet [<Post: Post object (1)>]>
>>>
```
save之后，有了Post object了。
但是显示的不怎么样友好。。。怎么办呢。 Post model 是我们自己写的。 可以改呀。。。

在models.py里加入
```python
    def __str__(self):
        return self.title
```
`__str__` dunder str。是应该叫什么打印方法？？。。。


之后重启shell就可以看到变化了。 
```python
 (django_env)   python manage.py shell 
Python 3.7.3 (default, Mar 27 2019, 16:54:48)
[Clang 4.0.1 (tags/RELEASE_401/final)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from blog.models import Post
>>> from django.contrib.auth.models import User
>>> Post.objects.all()
<QuerySet [<Post: Blog 1>]>
>>>
```

从`<Post: Post object (1)>` 变`<Post: Blog 1>`

继续
```python
>>> user = User.objects.filter(username='ShiningBridge').first()
>>> user
<User: ShiningBridge>
>>> post_2 = Post(title='Blog 二', content='第二个post的内容', author_id=user.id)
>>> Post.objects.all()
<QuerySet [<Post: Blog 1>, <Post: Blog 二>]>
>>> post = Post.objects.first()
>>> post.content
'First Post 内容'
>>> post.date_
post.date_error_message(  post.date_posted
>>> post.date_posted
datetime.datetime(2019, 6, 16, 20, 0, 40, 804013, tzinfo=<UTC>)
>>> post.author.email
'zcam01@gmail.com'
>>> user.post_set
<django.db.models.fields.related_descriptors.create_reverse_many_to_one_manager.<locals>.RelatedManager object at 0x111e5def0>
>>> user.post_set.all()
<QuerySet [<Post: Blog 1>, <Post: Blog 二>]>
>>> user.post_set.create(title='Blog 3', content='Third Post Content')
<Post: Blog 3>
```
关系数据库，可以互相联系起来。 用post 找user。 用user 找post。

* `post.author.email` 可以找user的email
* `user.post_set` 可以搞到user的所有post。 叫做`post_set`。
  - 规则是`<modelname>_set`，model名➕`_set`
* `user.post_set.create(title='Blog 3', content='Third Post Content')` 都不用save了。


### 把view改一下
views.py文件里， 不要在用static dummy data了。import我们的blog.models里的Post模型，用数据库提供内容。 
```python
from blog.models import Post
...
...
def home(request):
    context = {
        'posts': Post.objects.all()     ## 用database拉。
    }
    return render(request, 'blog/home.html', context)

```


### 日期格式
```html
<small class="text-muted">{{ post.date_posted | date:'F d, Y' }}</small>
```

Django Date Filters:
https://docs.djangoproject.com/en/2.0/ref/templates/builtins/#date

### admin.py

```python
from django.contrib import admin
from .models import Post

# Register your models here.
admin.site.register(Post)
```
用Django还可以给自由加入模块。比如我们的 Post
`admin.site.register(Post)`


