from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class BlogCategory(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-pub_time']

class BlogComment(models.Model):
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    blog = models.ForeignKey(Blog, related_name='comments',on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.content
    class Meta:
        ordering = ['-pub_time']
