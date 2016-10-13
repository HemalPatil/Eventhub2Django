# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_userprofile_loggedin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='collegeName',
            field=models.CharField(default=b'NIT', max_length=128),
        ),
    ]
