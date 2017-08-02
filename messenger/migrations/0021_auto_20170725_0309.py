# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-25 03:09
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('messenger', '0020_auto_20170720_0543'),
    ]

    operations = [
        migrations.CreateModel(
            name='SiteProfile',
            fields=[
                ('domain', models.CharField(max_length=512)),
                ('site_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='messagethread',
            name='status',
            field=models.CharField(choices=[('PU', 'PUBLIC'), ('PR', 'PRIVATE'), ('PE', 'PERSONAL')], default='PR', max_length=2),
        ),
        migrations.AlterField(
            model_name='archive',
            name='expiry',
            field=models.DateTimeField(default=datetime.datetime(2017, 7, 25, 3, 14, 47, 53145)),
        ),
        migrations.AddField(
            model_name='messagethread',
            name='site',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='messenger.SiteProfile'),
        ),
    ]