# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_auto_20151112_2008'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='mobile_id',
            field=models.CharField(default='now', max_length=300),
            preserve_default=False,
        ),
    ]
