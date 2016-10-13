# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evm', '0009_auto_20151118_1230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='subtype',
            field=models.CharField(default=b'general', max_length=128, choices=[(b'general', b'general'), (b'club', b'club'), (b'IG', b'IG'), (b'online', b'online'), (b'Branch', b'Branch')]),
        ),
    ]
