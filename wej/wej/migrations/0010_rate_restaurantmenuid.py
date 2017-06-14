# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-06-14 12:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wej', '0009_auto_20170614_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='restaurantMenuId',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='restaurantMenu_rel', to='wej.RestaurantMenu'),
        ),
    ]
