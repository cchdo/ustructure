from django.shortcuts import render, render_to_response, redirect
from django.conf import settings

from microstructure.models import Program


from tagstore.client import TagStoreClient, Query as TSQuery


tstore = TagStoreClient(settings.TAGSTORE_API_ENDPOINT)


def home(request):
    return redirect('programs')


def programs(request):
    programs = Program.objects.all()
    data = {'programs': programs}
    return render_to_response("programs.html", data)


class TSDataFileProxy(object):
    def __init__(self, tsdata):
        self.tsdata = tsdata

    @property
    def url(self):
        return self.tsdata.data.uri


class TSData(object):
    def __init__(self, data):
        self.data = data
        self.file_proxy = TSDataFileProxy(self)

    @property
    def filename(self):
        return self.data.filename

    @property
    def file(self):
        return self.file_proxy


def program(request, pid):
    program = Program.objects.get(id=pid)
    data = {}
    data['program'] = program

    query_base = [TSQuery.tags_any('eq', 'website:microstructure'),
                  TSQuery.tags_any('eq', 'program:{0}'.format(program.id))]

    data['dataset'] = map(TSData,
        tstore.query(TSQuery.tags_any('eq', 'data_type:hrp'), TSQuery.tags_any('eq', 'format:data'), *query_base))
    data['data_intermediate'] = map(TSData,
        tstore.query(TSQuery.tags_any('eq', 'data_type:hrp'), TSQuery.tags_any('eq', 'format:intermediate'), *query_base))
    data['data_raw'] = map(TSData,
        tstore.query(TSQuery.tags_any('eq', 'data_type:hrp'), TSQuery.tags_any('eq', 'format:raw'), *query_base))
    data['data_report'] = map(TSData,
        tstore.query(TSQuery.tags_any('eq', 'data_type:report'), *query_base))
    return render_to_response("program.html", data)
