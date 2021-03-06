# Generated by Django 3.2.9 on 2021-11-06 14:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0004_auto_20211106_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='dislike',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='recipe.recipe'),
        ),
        migrations.AddField(
            model_name='like',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='recipe.recipe'),
        ),
        migrations.AlterField(
            model_name='dislike',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='recipe.comment'),
        ),
        migrations.RemoveField(
            model_name='dislike',
            name='users',
        ),
        migrations.AddField(
            model_name='dislike',
            name='users',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requirement_comment_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='like',
            name='comment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='recipe.comment'),
        ),
        migrations.RemoveField(
            model_name='like',
            name='users',
        ),
        migrations.AddField(
            model_name='like',
            name='users',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='requirement_comment_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
