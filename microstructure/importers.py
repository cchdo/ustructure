import os
from csv import reader as csv_reader
import logging
log = logging.getLogger(__name__)

from django.core.files import File

from microstructure.models import Program, ProgramFile

from microstructure.views import tstore, TSQuery


def import_cruises_csv(csvfname):
    with open(csvfname, 'rb') as fff:
        reader = csv_reader(fff)
        reader.next()
        for row in reader:
            (allowed, name, ship, owner, pi, url, dates, port_start, port_end,
             institutions) = row
            program = Program.objects.filter(name=name).all()
            if program:
                program = program[0]
            else:
                program = Program()
            program.data_public = bool(allowed)
            program.name = name
            program.ship = ship
            program.owner = owner
            program.pi = pi
            program.url = url

            program.dates = dates

            program.port_start = port_start
            program.port_end = port_end

            institutions = [xxx.strip() for xxx in institutions.split(',')]
            program.institutions = ','.join(institutions)

            print program
            program.save()


def import_dir(dname):
    """Import a directory containing intermediate data, raw, and reports.

    An additional file program_id containing only the program id number should
    also be present for each directory.
    
    """
    print dname
    intermediates = os.listdir(dname)
    intermediates.remove('raw')
    intermediates.remove('report')
    intermediates.remove('program_id')

    program_id = open(os.path.join(dname, 'program_id'), 'r').read().strip()
    program = Program.objects.get(id=program_id)

    base_tags = ['website:microstructure', 'program:{0}'.format(program.id)]

    for fname in intermediates:
        tags = base_tags + ['data_type:hrp', 'format:intermediate']
        fobj = open(os.path.join(dname, fname))
        tstore.create(fobj, fname, tags)

    raw_dir = os.path.join(dname, 'raw')
    if os.path.isdir(raw_dir):
        for fname in os.listdir(raw_dir):
            tags = base_tags + ['data_type:hrp', 'format:raw']
            fobj = open(os.path.join(raw_dir, fname))
            tstore.create(fobj, fname, tags)

    report_dir = os.path.join(dname, 'report')
    if os.path.isdir(report_dir):
        for fname in os.listdir(report_dir):
            tags = base_tags + ['data_type:report']
            fobj = open(os.path.join(report_dir, fname))
            tstore.create(fobj, fname, tags)


def tstore_find(tags, *other, **kwargs):
    filters = [TSQuery.tags_any('eq', tag) for tag in tags] + other
    return tstore.query(*filters, **kwargs)


def import_data(program, path):
    """Import a file to a program as standarad data.
    
    """
    fname = os.path.basename(path)

    tags = ['website:microstructure', 'program:{0}'.format(program.id), 'data_type:hrp',  'format:data']
    pfile = tstore_find(tags, ['fname', 'eq', fname], single=True)

    fname = os.path.basename(path)
    fobj = open(path)
    if pfile:
        tstore.edit(pfile.id, fobj, fname, tags)
        log.info(u'Updated {0}'.format(fname))
    else:
        tstore.create(fobj, fname, tags)
        log.info(u'Imported {0}'.format(fname))
