# Generated by Django 3.1.5 on 2021-04-16 05:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0021_auto_20210416_1059'),
    ]

    operations = [
        migrations.AlterField(
            model_name='messages',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 16, 11, 18, 7, 67117)),
        ),
    ]
