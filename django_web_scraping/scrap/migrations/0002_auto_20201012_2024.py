# Generated by Django 3.1.2 on 2020-10-12 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='scrap',
            name='author',
        ),
        migrations.RemoveField(
            model_name='scrap',
            name='content',
        ),
        migrations.RemoveField(
            model_name='scrap',
            name='date_posted',
        ),
    ]
