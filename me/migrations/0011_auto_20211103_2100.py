# Generated by Django 3.1.1 on 2021-11-03 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('me', '0010_auto_20211101_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='myuser',
            name='moderator',
            field=models.BooleanField(default=False),
        ),
    ]
