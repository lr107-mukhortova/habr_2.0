# Generated by Django 3.1.1 on 2021-11-03 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_auto_20211103_1345'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='user',
            new_name='from_user',
        ),
    ]