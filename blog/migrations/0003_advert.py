# Generated by Django 4.2.1 on 2023-06-01 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_views'),
    ]

    operations = [
        migrations.CreateModel(
            name='Advert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('ad_type', models.CharField(choices=[('GIF', 'GIF'), ('IMAGE', 'Image'), ('VIDEO', 'Video')], max_length=10)),
                ('file', models.FileField(upload_to='advertisements/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
