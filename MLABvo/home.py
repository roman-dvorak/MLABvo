from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response

#from .models import Observatory
from .MLABvo import _sql, getProjects

def index(request):
    BZ_element = {'realTimeMap': ['RTbolidozor', "home/realtimeTile.png", "title"],
                  'multibolid': ['RTbolidozor', "home/multibolidTile.png", "title" ],
                  'data': ['RTbolidozor', "home/multibolidTile.png", "title" ],
                  'wiki': ['RTbolidozor', "home/multibolidTile.png", "title" ],
                  'space': ['RTbolidozor', "home/multibolidTile.png", "title" ],
                  'counts': ['RTbolidozors', "home/multibolidTile.png", "counts" ],
                  'api': ['api', "home/multibolidTile.png", "counts" ],}
    context = {'BZ_element': BZ_element, 'projects': ['Bolidozor', 'Ionozor']}

    return render(request, 'index.html', context)

def home(request):
    context = {'projects': getProjects()}
    return render(request, 'index.html', context)

