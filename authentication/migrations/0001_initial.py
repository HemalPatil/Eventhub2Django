# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('phoneNumber', models.CharField(max_length=30)),
                ('collegeName', models.CharField(max_length=128)),
                ('dateOfBirth', models.DateField()),
                ('signUpDate', models.DateField(auto_now=True)),
                ('picture', models.ImageField(upload_to=b'profile_pictures', blank=True)),
                ('ipaddress', models.URLField(max_length=25)),
                ('lastLoginDate', models.DateTimeField(blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
