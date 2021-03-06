# Generated by Django 3.2.9 on 2021-11-06 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_auto_20211106_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dislike',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='recipe.comment'),
        ),
        migrations.AlterField(
            model_name='dislike',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dislikes', to='recipe.recipe'),
        ),
        migrations.AlterField(
            model_name='like',
            name='comment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='recipe.comment'),
        ),
        migrations.AlterField(
            model_name='like',
            name='recipe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='recipe.recipe'),
        ),
    ]
