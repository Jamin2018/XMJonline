# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-10 03:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='citydict',
            options={'verbose_name': '机构', 'verbose_name_plural': '机构'},
        ),
    ]
