# Generated by Django 4.0.3 on 2022-03-23 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0002_alter_movie_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='category',
            field=models.CharField(default='Superhero', max_length=100),
            preserve_default=False,
        ),
    ]
