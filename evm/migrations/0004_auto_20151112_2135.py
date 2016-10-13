# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evm', '0003_auto_20151112_2111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='club',
            field=models.CharField(default=b'general', max_length=128, choices=[(b'DND', b'DND'), (b'music', b'music'), (b'quiz', b'quiz'), (b'DLD', b'DLD')]),
            preserve_default=True,
        ),
    ]
