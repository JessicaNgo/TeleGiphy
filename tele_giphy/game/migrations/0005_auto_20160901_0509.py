# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-01 05:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_gameoverrecords'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gameoverrecords',
            old_name='record',
            new_name='records',
        ),
    ]