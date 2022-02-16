from django.db import models
from django.db.models.deletion import CASCADE

from django.db.models.fields.related import OneToOneField


class MyUser(models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=120)
    password = models.CharField(max_length=120)

    avatar = models.ImageField(default="images/profile.jpg", upload_to='images')

    admin = models.BooleanField(default=False)
    moderator = models.BooleanField(default=False)

    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    def __str__(self) -> str:
        return str(self.email)


class Profile(models.Model):
    to_user = OneToOneField(MyUser, on_delete=CASCADE, primary_key=True)
    status = models.CharField(max_length=300, default='')
