import os.path

from django.db import models
from django.db.models import ForeignKey, FileField

class Program(models.Model):
    name = models.CharField(max_length=30)
    ship = models.CharField(max_length=30)
    # owner is aka data originator
    owner = models.CharField(max_length=30)
    pi = models.CharField(max_length=30)
    url = models.CharField(max_length=2**11)
    dates = models.CharField(max_length=30)
    port_start = models.CharField(max_length=30)
    port_end = models.CharField(max_length=30)
    institutions = models.CharField(max_length=30)
    data_public = models.BooleanField(default=False)
    data_policy = models.CharField(max_length=2**11, null=True)

    def __unicode__(self):
        return self.name


class ProgramFile(models.Model):
    FTYPES = (
        ('d', 'data'),
        ('i', 'intermediate'),
        ('0', 'raw'),
        ('r', 'report'),
    )

    owner = ForeignKey(Program)
    ftype = models.CharField(max_length=1, choices=FTYPES)
    filename = models.CharField(max_length=512)
    file = FileField(upload_to='data')

    def __unicode__(self):
        return u'{0} {1} {2} {3}'.format(self.id, self.owner, self.ftype,
                                         self.filename)
