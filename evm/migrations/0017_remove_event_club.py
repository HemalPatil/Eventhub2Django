# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evm', '0016_club_userfollow'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='club',
        ),
    ]
