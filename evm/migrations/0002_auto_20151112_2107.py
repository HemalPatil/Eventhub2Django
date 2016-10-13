# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='description',
            field=models.TextField(max_length=128),
            preserve_default=True,
        ),
    ]
