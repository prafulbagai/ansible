# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-03-15 10:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_auto_20170220_1237'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnavailableCodesHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('device_id', models.IntegerField(db_index=True)),
                ('master_name', models.CharField(db_index=True, max_length=255)),
                ('date', models.DateTimeField(auto_now=True, db_index=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='unavailablecodes',
            name='group_name',
        ),
        migrations.AlterField(
            model_name='unavailablecodes',
            name='count',
            field=models.IntegerField(db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='unavailablecodes',
            name='master_name',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
