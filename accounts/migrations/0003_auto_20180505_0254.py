# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-05-04 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_medicine_amount'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=10, null=True)),
                ('name', models.CharField(max_length=10, null=True)),
                ('message', models.CharField(max_length=10, null=True)),
                ('email', models.EmailField(max_length=254)),
                ('date', models.DateField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='cityareamapping',
            unique_together=set([('city', 'area')]),
        ),
    ]
