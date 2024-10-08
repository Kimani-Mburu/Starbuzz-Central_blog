# Generated by Django 4.2.1 on 2023-05-30 15:38

import ckeditor.fields
import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import versatileimagefield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True)),
                ('website', models.URLField(blank=True)),
                ('profile_image', models.ImageField(blank=True, upload_to='profile_images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Title')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, max_length=250, null=True, unique=True)),
                ('status', models.CharField(choices=[('published', 'Published'), ('draft', 'Draft')], default='draft', max_length=10, verbose_name='status')),
                ('publication_date', models.DateTimeField(verbose_name='Created')),
                ('picture', versatileimagefield.fields.VersatileImageField(blank=True, height_field='height', null=True, upload_to='blog-uploads/%Y/', verbose_name='Picture as thumbnail', width_field='width')),
                ('height', models.PositiveIntegerField(blank=True, null=True, verbose_name='Profile Image Height')),
                ('width', models.PositiveIntegerField(blank=True, null=True, verbose_name='Profile Image Width')),
                ('picture_description', models.CharField(max_length=127, verbose_name='description of the image')),
                ('post_excerpt', ckeditor.fields.RichTextField(verbose_name='post excerpt')),
                ('post_content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='post content')),
                ('is_featured', models.BooleanField(default=False, verbose_name='Is the post feature or not?')),
                ('author', models.CharField(default='Anonymous', max_length=64, verbose_name='Created by')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.category', verbose_name='Category')),
                ('tags', models.ManyToManyField(to='blog.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='blog.post')),
            ],
        ),
    ]
