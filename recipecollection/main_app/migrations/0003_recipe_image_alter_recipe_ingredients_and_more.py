# Generated by Django 5.0.6 on 2024-06-25 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_rename_cuisine_recipe_cuisine_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='image',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='recipe',
            name='ingredients',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='instructions',
            field=models.TextField(),
        ),
    ]
