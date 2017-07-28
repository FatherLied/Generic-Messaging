# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-10 08:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0002_auto_20170707_0709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilethread',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='copies', to='messenger.MessageThread'),
        ),
        migrations.AlterField(
            model_name='profilethread',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thread_copies', to='messenger.Profile'),
        ),
    ]
