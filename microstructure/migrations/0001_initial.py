# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('ship', models.CharField(max_length=30)),
                ('owner', models.CharField(max_length=30)),
                ('pi', models.CharField(max_length=30)),
                ('url', models.CharField(max_length=30)),
                ('dates', models.CharField(max_length=30)),
                ('port_start', models.CharField(max_length=30)),
                ('port_end', models.CharField(max_length=30)),
                ('institutions', models.CharField(max_length=30)),
                ('data_public', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProgramFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ftype', models.CharField(max_length=1, choices=[(b'd', b'data'), (b'i', b'intermediate'), (b'0', b'raw'), (b'r', b'report')])),
                ('file', models.FileField(upload_to=b'data')),
                ('owner', models.ForeignKey(to='microstructure.Program')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
