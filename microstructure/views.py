from django.shortcuts import render, render_to_response, redirect

from microstructure.models import Program


def home(request):
    return redirect('programs')


def programs(request):
    programs = Program.objects.all()
    data = {'programs': programs}
    return render_to_response("programs.html", data)


def program(request, pid):
    program = Program.objects.get(id=pid)
    data = {}
    data['program'] = program
    data['dataset'] = program.programfile_set.filter(ftype='d').all()
    data['data_intermediate'] = \
        program.programfile_set.filter(ftype='i').all()
    data['data_raw'] = \
        program.programfile_set.filter(ftype='0').all()
    data['data_report'] = \
        program.programfile_set.filter(ftype='r').all()
    return render_to_response("program.html", data)
