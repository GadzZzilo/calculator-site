# Generated by Django 4.2.5 on 2024-04-01 13:34

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(max_length=50, verbose_name='Никнейм')),
                ('first_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('middle_name', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('last_name', models.CharField(max_length=50, verbose_name='Отчество')),
                ('photo', models.ImageField(upload_to='authors_photos', verbose_name='Фото')),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('short_description', models.CharField(max_length=300, verbose_name='Краткое описание')),
                ('content', ckeditor.fields.RichTextField(verbose_name='Содержание')),
                ('photo', models.ImageField(upload_to='article_photos', verbose_name='Фото')),
                ('slug', models.SlugField(verbose_name='URL')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author', to='integrals.author', verbose_name='Автор')),
            ],
        ),
    ]