# Generated by Django 3.0.8 on 2020-11-15 13:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_news_views'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='photo',
        ),
    ]
