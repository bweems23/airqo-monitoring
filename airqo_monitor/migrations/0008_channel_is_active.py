# Generated by Django 2.1.2 on 2018-11-02 06:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airqo_monitor', '0007_auto_20181101_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='channel',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]