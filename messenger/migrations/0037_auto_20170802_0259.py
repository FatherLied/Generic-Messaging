# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 02:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0036_auto_20170802_0125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archive',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 2, 3, 4, 26, 921137, tzinfo=utc)),
        ),
    ]