# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2017-02-28 11:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stm_app', '0004_auto_20170228_0841'),
    ]

    operations = [
        migrations.CreateModel(
            name='Split',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='persons',
        ),
        migrations.AddField(
            model_name='split',
            name='project',
            field=models.ManyToManyField(to='stm_app.Project'),
        ),
        migrations.AddField(
            model_name='split',
            name='split',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
