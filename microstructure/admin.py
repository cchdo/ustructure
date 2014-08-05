from django.contrib import admin

# Register your models here.
from microstructure.models import Program, ProgramFile

admin.site.register(Program)
admin.site.register(ProgramFile)
