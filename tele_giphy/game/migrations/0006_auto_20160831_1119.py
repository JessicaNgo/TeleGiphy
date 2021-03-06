# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 11:19
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_gifchainnode_user_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gifchainnode',
            name='giphy_url',
            field=models.CharField(blank=True, max_length=2083),
        ),
        migrations.AlterField(
            model_name='gifchainnode',
            name='next_node',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='previous_node', to='game.GifChainNode'),
        ),
        migrations.AlterField(
            model_name='gifchainnode',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gif_owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='gifchainnode',
            name='user_text',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AlterField(
            model_name='gifchainstarter',
            name='first_node',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='game.GifChainNode'),
        ),
    ]
