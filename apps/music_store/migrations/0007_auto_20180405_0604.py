# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-05 06:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('music_store', '0006_auto_20180405_0547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paymentaccount',
            name='default_method',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='default_method', to='music_store.PaymentMethod'),
        ),
        migrations.AlterField(
            model_name='paymentaccount',
            name='methods_used',
            field=models.ManyToManyField(null=True, related_name='methods_used', to='music_store.PaymentMethod'),
        ),
    ]
