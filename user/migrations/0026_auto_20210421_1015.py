# Generated by Django 3.1.5 on 2021-04-21 04:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0025_auto_20210421_0858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 21, 10, 15, 14, 644891)),
        ),
    ]
