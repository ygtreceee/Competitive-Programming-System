# Generated by Django 5.0.4 on 2024-05-10 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_category_favoriteproblem'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProblemSet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(verbose_name='pNumber')),
                ('title', models.CharField(max_length=50, verbose_name='name')),
                ('content', models.TextField(verbose_name='content')),
                ('url', models.CharField(max_length=50, verbose_name='url')),
            ],
        ),
    ]
