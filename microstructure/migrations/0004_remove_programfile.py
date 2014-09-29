# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('microstructure', '0003_programfile_filename'),
    ]

    operations = [
        migrations.Deletemodel(
            model_name='programfile',
        ),
    ]
