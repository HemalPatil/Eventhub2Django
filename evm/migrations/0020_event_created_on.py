# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evm', '0019_auto_20151216_1119'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='created_on',
            field=models.DateTimeField(default=b'2016-05-16 20:00:00'),
        ),
    ]
