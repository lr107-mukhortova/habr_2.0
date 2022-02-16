from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey
from me.models import MyUser


class Post(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    model_name = models.CharField(max_length=200)
    short_description = models.TextField(max_length=700)

    full_description = models.TextField()

    ref_on_git = models.CharField(max_length=200)

    rating = models.FloatField(default=0)
    user = models.ForeignKey(MyUser, on_delete=CASCADE)


class Comment(models.Model):
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    body = models.TextField()

    to_post = ForeignKey(Post, on_delete=CASCADE)

    from_user = ForeignKey(MyUser, on_delete=CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=120)
    to_post = models.ManyToManyField(Post)
