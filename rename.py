#!/usr/bin/env python

import sys
import os
from shutil import move
from json import load as json_load, dump as json_dump
from contextlib import contextmanager
from zipfile import ZipFile
import tempfile

import logging


logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microstructure.settings")
from django.conf import settings
import django
django.setup()

from django.core.files import File

from microstructure.models import Program


def usage(prog):
    print 'Usage: {0} <csv file>'.format(prog)


def main(argv):
    if len(argv) < 1:
        usage(argv[0])
        return 1

    resp = ops.tstore.query(Query.tags_any('eq', u'website:microstructure'),
                            Query.tags_any('eq', u'data_type:hrp'),
                            Query.tags_any('eq', u'format:intermediate'))
    for data in resp:
        fname = data.fname.replace('_for_map', '_preprocessed')
        ops.tstore.edit(data.id, data.uri, fname, data.tags)

    resp = ops.tstore.query(Query.tags_any('eq', u'website:microstructure'),
                            Query.tags_any('eq', u'data_type:hrp'),
                            Query.tags_any('eq', u'format:data'))
    for data in resp:
        fname = data.fname.replace('_for_map', '')
        ops.tstore.edit(data.id, data.uri, data.fname, tags)

    return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv))

