# Generated by Django 4.2.1 on 2023-06-01 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_advert'),
    ]

    operations = [
        migrations.AddField(
            model_name='advert',
            name='link',
            field=models.URLField(blank=True, null=True),
        ),
    ]
