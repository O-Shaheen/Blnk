# Generated by Django 4.0.5 on 2022-06-13 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loaner',
            name='dueMoney',
            field=models.IntegerField(default=0),
        ),
    ]
