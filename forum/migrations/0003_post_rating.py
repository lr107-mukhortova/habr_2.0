# Generated by Django 3.1.1 on 2021-11-02 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_remove_post_tags'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='rating',
            field=models.FloatField(default=0),
        ),
    ]