# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evm', '0012_auto_20151118_2303'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('message', models.TextField(max_length=100)),
                ('event', models.ForeignKey(related_name='notifevent', to='evm.Event')),
            ],
        ),
        migrations.AlterField(
            model_name='content',
            name='description',
            field=models.TextField(max_length=500),
        ),
    ]
