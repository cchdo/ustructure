#!/usr/bin/env python

import sys
import os
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

from netCDF4 import Dataset

from tagstore.client import TagStoreClient, Query

from microstructure.models import Program, ProgramFile
from microstructure.importers import import_cruises_csv, import_dir, import_data


def usage(prog):
    print 'Usage: {0} <csv file>'.format(prog)


def _for_dirs(dirpath):
    for dname in os.listdir(dirpath):
        dpath = os.path.join(dirpath, dname)
        if not os.path.isdir(dpath):
            continue
        if dname.startswith('.'):
            continue
        yield dname, dpath


def import_processed_directory(dirpath):
    """Import a directory of directories of netCDF files.

    Each directory should be named as the program id.

    """
    for dname, dpath in _for_dirs(dirpath):
        program = Program.objects.get(id=dname)

        for fname in os.listdir(dpath):
            if not fname.endswith('.zip'):
                continue
            else:
                path = os.path.join(dpath, fname)
                import_data(program, path)


def rejoin_as_csv(string):
    return ','.join([x.strip() for x in string.split(',')])


def update_hrp_cfgs(dirpath):
    """Update the HRP configuration with data originators

    """
    for dname, dpath in _for_dirs(dirpath):
        fpath = os.path.join(dpath, 'hrp.cfg')
        try:
            with open(fpath, 'r') as fff:
                json = json_load(fff)
        except ValueError:
            log.error(u'Unable to read hrp.cfg for {0}'.format(dname))
            continue

        program = Program.objects.get(id=dname)
        json['pi'] = rejoin_as_csv(program.pi)
        json['originator'] = rejoin_as_csv(program.owner)

        with open(fpath, 'w') as fff:
            json_dump(
                json, fff, sort_keys=True, indent=2, separators=(',', ': '))


def update_zip_ncs(zfile, hrp_cfg):
    for info in zfile.infolist():
        tmp = tempfile.NamedTemporaryFile()
        tmp.write(zfile.read(info))
        tmp.flush()
        tmp.seek(0)
        try:
            # netcdf library wants to write its own files.
            nc_file = Dataset(tmp.name, 'a')
            try:
                try:
                    nc_file.pi = hrp_cfg['pi']
                except KeyError:
                    pass
                try:
                    nc_file.data_originator = hrp_cfg['originator']
                except KeyError:
                    pass
            finally:
                nc_file.close()
        finally:
            tmp.seek(0)
            zfile.writestr(info, tmp.read())
            tmp.close()


def update_nczips(dirpath):
    for dname, dpath in _for_dirs(dirpath):
        fpath = os.path.join(dpath, 'hrp.cfg')
        with open(fpath, 'r') as fff:
            json = json_load(fff)

        for fname in os.listdir(dpath):
            if not fname.endswith('.zip'):
                continue
            fpath = os.path.join(dpath, fname)
            with ZipFile(fpath, 'a') as zfile:
                update_zip_ncs(zfile, json)


def rename():
    tstore = TagStoreClient('http://hdo.ucsd.edu:53000/api/v1')

    resp = tstore.query_data(Query.tags_any('eq', u'website:microstructure'),
                            Query.tags_any('eq', u'data_type:hrp'),
                            Query.tags_any('eq', u'format:intermediate'))
    for data in resp:
        fname = data.fname.replace('_for_map', '_preprocessed')
        tstore.edit(data.id, data.uri, fname, data.tags)

    resp = tstore.query_data(Query.tags_any('eq', u'website:microstructure'),
                            Query.tags_any('eq', u'data_type:hrp'),
                            Query.tags_any('eq', u'format:data'))
    for data in resp:
        fname = data.fname.replace('_for_map', '')
        tstore.edit(data.id, data.uri, fname, data.tags)


def main(argv):
    if len(argv) < 1:
        usage(argv[0])
        return 1

    #import_cruises_csv(argv[1])

    dirpath = argv[1]

    ## import a directory containing directories of Programs. Each Program
    ## directory must include a program_id file.
    ## ~/Documents/data/microstructure_from_amy_2014-06
    #for dname in os.listdir(dirpath):
    #    if dname.startswith('.'):
    #        continue
    #    path = os.path.join(dirpath, dname)
    #    if not os.path.isdir(path):
    #        continue
    #    import_dir(path)

    # import the netCDF reformatted data
    import_processed_directory(dirpath)
    rename()

    #update_hrp_cfgs(dirpath)

    #update_nczips(dirpath)

    return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv))

