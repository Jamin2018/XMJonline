# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-12 06:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0005_auto_20180112_0607'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='用户'),
        ),
    ]
