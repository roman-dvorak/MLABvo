from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .MLABvo import _sql
import datetime

#from .models import Observatory

@method_decorator(csrf_exempt)
def tap(request=None, path=None):
    print "TAP API"
    print request
    print path
    return HttpResponse("You're looking at question")

@method_decorator(csrf_exempt)
def sync(request):
    print request
    return HttpResponse("You're looking at question")





def upload(request, project):
    print "Upload request for ", project
    if project ==  'bolidozor':
        requestType = str(request.GET.get('requestType', 'dataUploaded'))
        
        if requestType == "dataUploaded":

            filename = str(request.GET.get('filename', None))
            filename_original = str(request.GET.get('filename_original', filename))
            filepath = str(request.GET.get('filepath', None))
            checksum = str(request.GET.get('checksum', None))
            id_observer = int(request.GET.get('id_station', 0))
            station = str(request.GET.get('station', None))
            id_server = int(request.GET.get('id_server', 1)) # 1 je space.astro.cz
            uploadtime = str(request.GET.get('uploadtime', datetime.datetime.now()))
            lastaccestime = str(request.GET.get('lastaccestime', datetime.datetime.now()))
            indextime = str(request.GET.get('indextime', '0000-00-00 00:00:00'))


            _sql("REPLACE INTO `MLABvo`.`bolidozor_fileindex` SET `filename_original` = '%s', `filename` = '%s', `id_observer` = '%d', `id_server` = '%d', `filepath` = '%s', `obstime` = '%s', `uploadtime` = '%s', `lastaccestime` = '%s', `indextime` = '%s', `checksum` = '%s'"
                %(filename_original, filename, id_observer, id_server, filepath, uploadtime, uploadtime, lastaccestime, indextime, checksum))

            return HttpResponse("ACK<br> New file was indexed")

