# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-01 02:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20160830_1009'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameOverRecords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('record', models.CharField(max_length=500000)),
            ],
        ),
    ]