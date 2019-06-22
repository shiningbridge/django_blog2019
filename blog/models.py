from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 100)
    content = models.TextField()
    date_posted = models.DateTimeField(default = timezone.now)  ## timezone.now后边不加括号()，因为不想让他执行，只是引用
    ## auto_now=True老是变... auto_now_add=True完全不变
    author = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
