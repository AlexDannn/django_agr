# Generated by Django 3.1.2 on 2020-10-14 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='category',
            field=models.CharField(default='Other', max_length=20),
        ),
    ]
