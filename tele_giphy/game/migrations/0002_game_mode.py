# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-30 08:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='mode',
            field=models.CharField(default='hotseat', max_length=20),
        ),
    ]