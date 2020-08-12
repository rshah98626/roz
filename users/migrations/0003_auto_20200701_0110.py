#  Copyright (c) 2020. Property of Wonderwerk, all rights reserved.

# Generated by Django 3.0.6 on 2020-07-01 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_customerprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerprofile',
            name='cents',
            field=models.IntegerField(default=0, verbose_name='money in the account (cents)'),
        ),
    ]