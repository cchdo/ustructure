#!/usr/bin/env python

import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microstructure.settings")
from django.conf import settings

from microstructure.models import Program
from microstructure.importers import import_cruises_csv, import_dir, import_data


def usage(prog):
    print 'Usage: {0} <csv file>'.format(prog)


def main(argv):
    if len(argv) < 1:
        usage(argv[0])
        return 1

    #import_cruises_csv(argv[1])

    # import a directory containing directories of Programs. Each Program
    # directory must include a program_id file.
    #path = argv[1]
    #for dname in os.listdir(path):
    #    import_dir(os.path.join(path, dname))


    # import a directory of directories of netCDF files. Each directory should
    # be named as the program id.
    dirpath = argv[1]
    for dname in os.listdir(dirpath):
        dpath = os.path.join(dirpath, dname)
        if not os.path.isdir(dpath):
            continue
        if dname.startswith('.'):
            continue
        program = Program.objects.get(id=dname)

        for fname in os.listdir(dpath):
            if not fname.endswith('.zip'):
                continue
            pfiles = program.programfile_set.filter(ftype='d').all()
            fnames = [p.filename for p in pfiles]
            if fname in fnames:
                continue
            import_data(program, os.path.join(dpath, fname))
    return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv))

