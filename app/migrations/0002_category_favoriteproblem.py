# Generated by Django 5.0.4 on 2024-05-05 12:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteProblem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='title')),
                ('link', models.CharField(max_length=50, verbose_name='link')),
                ('description', models.CharField(max_length=50, verbose_name='description')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='create_time')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.category', verbose_name='category')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userinfo')),
            ],
        ),
    ]