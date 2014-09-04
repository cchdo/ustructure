import os
from csv import reader as csv_reader

from django.core.files import File

from microstructure.models import Program, ProgramFile


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

    for fname in intermediates:
        pff = ProgramFile(owner=program,
                          ftype='i',
                          filename=fname,
                          file=File(open(os.path.join(dname, fname))))
        pff.save()


    raw_dir = os.path.join(dname, 'raw')
    if os.path.isdir(raw_dir):
        for fname in os.listdir(raw_dir):
            pff = ProgramFile(owner=program,
                              ftype='0',
                              filename=fname,
                              file=File(open(os.path.join(raw_dir, fname))))
            pff.save()

    report_dir = os.path.join(dname, 'report')
    if os.path.isdir(report_dir):
        for fname in os.listdir(report_dir):
            pff = ProgramFile(owner=program,
                              ftype='r',
                              filename=fname,
                              file=File(open(os.path.join(report_dir, fname))))
            pff.save()


def import_data(program, path):
    """Import a file to a program as standarad data.
    
    """
    pff = ProgramFile(owner=program, ftype='d', filename=os.path.basename(path),
                      file=File(open(path)))
    pff.save()
