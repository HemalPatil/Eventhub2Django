# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sectionscore',
            name='score',
        ),
        migrations.RemoveField(
            model_name='sectionscore',
            name='total',
        ),
        migrations.AddField(
            model_name='sectionscore',
            name='email',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sectionscore',
            name='is_android',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='sectionscore',
            name='is_download',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sectionscore',
            name='number',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='sectionscore',
            name='rollno',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
