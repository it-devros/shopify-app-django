# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-27 02:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

  dependencies = [
    ('main_app', '0001_initial'),
  ]

  operations = [
    migrations.CreateModel(
      name='Times',
      fields=[
        ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
        ('shop_name', models.CharField(editable=False, max_length=255, unique=True)),
        ('days', models.CharField(max_length=255)),
        ('hours', models.CharField(max_length=255)),
        ('mins', models.CharField(max_length=255)),
        ('secs', models.CharField(max_length=255)),
      ],
    ),
  ]
