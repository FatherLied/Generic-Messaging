# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 06:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0023_auto_20170725_0550'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteprofile',
            name='company_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=32),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='archive',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 25, 6, 41, 31, 607235)),
        ),
    ]
