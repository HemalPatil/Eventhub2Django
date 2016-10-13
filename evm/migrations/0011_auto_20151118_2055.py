# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evm', '0010_auto_20151118_2054'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='club',
            field=models.CharField(default=b'general', max_length=128, choices=[(b'DND', b'DND'), (b'music', b'music'), (b'quiz', b'quiz'), (b'DLD', b'DLD'), (b'Painting', b'Painting'), (b'LND', b'LND'), (b'PGC', b'PGC'), (b'Science and Hobbies', b'Science and Hobbies'), (b'EA-HAM', b'EA-HAM'), (b'Value Education', b'Value Education'), (b'Innovation', b'Innovation'), (b'Film', b'Film'), (b'ISE', b'ISE'), (b'ISTE', b'ISTE'), (b'Youth Red Cross', b'Youth Red Cross'), (b'FISA', b'FISA'), (b'Magazine', b'Magazine'), (b'HoneyBee', b'HoneyBee'), (b'SpicMacay', b'SpicMacay'), (b'Radio', b'Radio'), (b'Branch', b'Branch')]),
        ),
    ]
