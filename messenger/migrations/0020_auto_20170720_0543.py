# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-20 05:43
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0019_merge_20170720_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 20, 5, 48, 5, 970599)),
        ),
    ]
