# Generated by Django 3.1.2 on 2020-10-14 20:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0003_scrap_users_list'),
        ('users', '0006_auto_20201014_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_list', to='scrap.scrap'),
        ),
    ]