# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-03 20:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20160903_2045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gameoverrecords',
            name='game_token',
            field=models.CharField(max_length=16),
        ),
    ]