#!/usr/bin/env python

import sys
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microstructure.settings")
from django.conf import settings

from microstructure.importers import import_cruises_csv, import_dir


def usage(prog):
    print 'Usage: {0} <csv file>'.format(prog)


def main(argv):
    if len(argv) < 1:
        usage(argv[0])
        return 1

    import_cruises_csv(argv[1])

    #path = argv[1]
    #for dname in os.listdir(path):
    #    import_dir(os.path.join(path, dname))
    return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv))

