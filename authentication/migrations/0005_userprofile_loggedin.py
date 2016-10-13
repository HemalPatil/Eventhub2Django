# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_auto_20151112_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='loggedIn',
            field=models.BooleanField(default=False),
        ),
    ]
