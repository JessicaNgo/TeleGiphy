# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_gifchainnode_gifchainstarter'),
    ]

    operations = [
        migrations.AddField(
            model_name='gifchainnode',
            name='user_text',
            field=models.CharField(default='hello', max_length=150),
            preserve_default=False,
        ),
    ]