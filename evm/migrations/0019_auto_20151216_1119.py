# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import evm.models
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('evm', '0018_event_club'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(null=True, upload_to=evm.models.get_image_path, blank=True),
        ),
    ]
