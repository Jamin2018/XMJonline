# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-15 00:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0009_auto_20180112_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseorg',
            name='tag',
            field=models.CharField(default='世界名校', max_length=10, verbose_name='机构标签'),
        ),
    ]
