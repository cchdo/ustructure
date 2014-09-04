# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os.path

from django.db import models, migrations


def set_filenames(apps, schema_editor):
    # We can't import the ProgramFile model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    ProgramFile = apps.get_model("microstructure", "ProgramFile")
    for pfile in ProgramFile.objects.all():
        pfile.filename = os.path.basename(pfile.file.name)
        pfile.save()


class Migration(migrations.Migration):

    dependencies = [
        ('microstructure', '0002_auto_20140903_1959'),
    ]

    operations = [
        migrations.AddField(
            model_name='programfile',
            name='filename',
            field=models.CharField(default='', max_length=512),
            preserve_default=False,
        ),
        migrations.RunPython(set_filenames),
    ]
