# Generated by Django 3.1.1 on 2021-11-01 12:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('me', '0007_auto_20211029_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(default='profile.jpg', upload_to='images'),
        ),
    ]
