# Generated by Django 2.1.2 on 2018-10-31 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airqo_monitor', '0005_auto_20181025_0953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='resolved_at',
            field=models.DateTimeField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='malfunctionreason',
            name='name',
            field=models.TextField(db_index=True),
        ),
    ]
