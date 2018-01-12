# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-12 06:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0005_auto_20180112_0518'),
        ('operation', '0006_auto_20180112_0610'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercourse',
            name='course',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='courses.Course', verbose_name='课程'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usercourse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='operation.UserMessage', verbose_name='用户'),
        ),
    ]