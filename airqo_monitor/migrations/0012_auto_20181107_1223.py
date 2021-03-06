# Generated by Django 2.1.2 on 2018-11-07 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airqo_monitor', '0011_globalvariable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channeltype',
            name='data_format_json',
            field=models.TextField(help_text='JSON map of the external fields to helpful python fieldnames (e.g. {"field1": "pm_1","field2": "pm_2_5","field3": "pm_10","field4": "sample_period","field5": "latitude","field6": "longitude","field7": "battery_voltage"})'),
        ),
        migrations.AlterField(
            model_name='channeltype',
            name='name',
            field=models.TextField(db_index=True, help_text="This must match the channel's tag on the Thingspeak"),
        ),
    ]
