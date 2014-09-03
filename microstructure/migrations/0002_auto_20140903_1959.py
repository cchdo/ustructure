# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microstructure', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='data_policy',
            field=models.CharField(max_length=2048, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='program',
            name='url',
            field=models.CharField(max_length=2048),
        ),
    ]
