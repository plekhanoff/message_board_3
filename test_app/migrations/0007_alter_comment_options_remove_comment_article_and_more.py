# Generated by Django 5.0.2 on 2024-03-04 15:20

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('test_app', '0006_alter_user_managers'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['id'], 'verbose_name': 'комментарий', 'verbose_name_plural': 'комментарий'},
        ),
        migrations.RemoveField(
            model_name='comment',
            name='article',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.AddField(
            model_name='comment',
            name='commentArticle',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='test_app.article', verbose_name='комментарий'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='commentUser',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='comment',
            name='status',
            field=models.BooleanField(default=False, verbose_name='статус'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='время создания'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(verbose_name='коммент'),
        ),
    ]