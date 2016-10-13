# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.datetime_safe


class Migration(migrations.Migration):

    dependencies = [
        ('evm', '0013_auto_20151120_1459'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='addedon',
            field=models.DateTimeField(default=django.utils.datetime_safe.datetime.now, auto_now=True),
            preserve_default=False,
        ),
    ]
