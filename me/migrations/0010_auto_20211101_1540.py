# Generated by Django 3.1.1 on 2021-11-01 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('me', '0009_auto_20211101_1537'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='avatar',
            field=models.ImageField(default='images/profile.jpg', upload_to='images'),
        ),
    ]
