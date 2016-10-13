# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evm', '0002_auto_20151112_2107'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='content',
        ),
        migrations.AddField(
            model_name='content',
            name='event',
            field=models.OneToOneField(related_name='content', default=1, to='evm.Event'),
            preserve_default=False,
        ),
    ]
