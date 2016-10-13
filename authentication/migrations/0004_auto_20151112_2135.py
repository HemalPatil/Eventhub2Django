# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_userprofile_mobile_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='mobile_id',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
