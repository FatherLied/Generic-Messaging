# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 07:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0033_merge_20170728_0600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 28, 7, 34, 51, 375281)),
        ),
    ]