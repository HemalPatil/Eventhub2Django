# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('evm', '0005_userevents'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventRatings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField(default=0)),
                ('feedback', models.TextField(max_length=300)),
                ('event', models.ForeignKey(related_name='eventfeedback', to='evm.Event')),
                ('user', models.ForeignKey(related_name='userfeedback', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
