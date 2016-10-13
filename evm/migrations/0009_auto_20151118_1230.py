# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evm', '0008_auto_20151118_0014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='alias',
            field=models.CharField(unique=True, max_length=128),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(unique=True, max_length=128),
        ),
    ]
