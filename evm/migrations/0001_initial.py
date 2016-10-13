# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import evm.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(null=True, upload_to=evm.models.get_image_path, blank=True)),
                ('description', models.TextField(max_length=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'event', max_length=128, choices=[(b'event', b'event'), (b'workshop', b'workshop'), (b'lecture', b'lecture'), (b'attraction', b'attraction')])),
                ('subtype', models.CharField(default=b'general', max_length=128, choices=[(b'general', b'general'), (b'club', b'club'), (b'IG', b'IG'), (b'online', b'online')])),
                ('club', models.CharField(default=b'general', max_length=128, choices=[(b'general', b'general'), (b'club', b'club'), (b'IG', b'IG'), (b'online', b'online')])),
                ('name', models.CharField(max_length=128)),
                ('date_time', models.DateTimeField()),
                ('contact_name_1', models.CharField(max_length=128)),
                ('contact_number_1', models.CharField(max_length=10)),
                ('contact_name_2', models.CharField(max_length=128)),
                ('contact_number_2', models.CharField(max_length=10)),
                ('venue', models.CharField(max_length=128)),
                ('alias', models.CharField(max_length=128)),
                ('content', models.OneToOneField(related_name='event', to='evm.Content')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
