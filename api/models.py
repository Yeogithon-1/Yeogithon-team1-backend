from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(max_length=100, unique=True)


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    content = models.TextField()
    tag = models.CharField(max_length=10, default="", null=True, blank=True)
    like = models.ManyToManyField(
        User, related_name='postlike', blank=True)


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def all2(self):
        qs = super(CommentManager, self)
        return qs


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comment')
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=200)
    parent = models.ForeignKey(
        'self', related_name='replies', on_delete=models.CASCADE, null=True, blank=True)
    like = models.ManyToManyField(
        User, related_name='like', blank=True)

    # objects = CommentManager()

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True
