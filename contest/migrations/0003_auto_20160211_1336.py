# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contest', '0002_auto_20160211_0632'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sectionscore',
            name='number',
        ),
        migrations.RemoveField(
            model_name='sectionscore',
            name='rollno',
        ),
    ]
