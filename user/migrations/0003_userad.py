# Generated by Django 3.1.5 on 2021-03-23 17:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
        ('user', '0002_auto_20210316_1003'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.CharField(max_length=10)),
                ('km_driven', models.DecimalField(decimal_places=2, max_digits=10)),
                ('title', models.CharField(max_length=20)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField()),
                ('image1', models.ImageField(upload_to='image')),
                ('image2', models.ImageField(upload_to='image')),
                ('image3', models.ImageField(upload_to='image')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.brands')),
            ],
        ),
    ]
