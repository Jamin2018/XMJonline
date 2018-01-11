# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-01-11 02:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20180110_0300'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='citydict',
            options={'verbose_name': '城市', 'verbose_name_plural': '城市'},
        ),
        migrations.AlterModelOptions(
            name='courseorg',
            options={'verbose_name': '机构详情', 'verbose_name_plural': '机构详情'},
        ),
        migrations.AddField(
            model_name='courseorg',
            name='category',
            field=models.CharField(choices=[('pxjg', '培训机构'), ('gx', '高校'), ('gr', '个人')], default='pxjg', max_length=20, verbose_name='机构类别'),
        ),
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(upload_to='org/%Y/%m', verbose_name='logo'),
        ),
    ]
