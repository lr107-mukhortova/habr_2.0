# Generated by Django 3.1.1 on 2021-11-01 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('me', '0010_auto_20211101_1540'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('model_name', models.CharField(max_length=200)),
                ('short_description', models.TextField()),
                ('full_description', models.TextField()),
                ('tags', models.TextField()),
                ('ref_on_git', models.CharField(max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='me.myuser')),
            ],
        ),
    ]
