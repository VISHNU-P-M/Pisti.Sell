# Generated by Django 3.1.5 on 2021-04-21 03:28

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0024_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='userad',
            name='fuel',
            field=models.CharField(max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='messages',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 4, 21, 8, 58, 41, 693134)),
        ),
    ]
