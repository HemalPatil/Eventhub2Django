# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='dateOfBirth',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='phoneNumber',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='picture',
        ),
    ]
