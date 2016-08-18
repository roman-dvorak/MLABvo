from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.shortcuts import render

#from models.MLABvo import VoFileindex
#from models.Project import AuthUser

import MySQLdb as mdb

def _sql(query, read=False, db = 'MLABvo'):
        print "#>", query
        connection = mdb.connect(host="localhost", user="root", passwd="root", db=db, use_unicode=True, charset="utf8")
        cursorobj = connection.cursor()
        result = None
        try:
                cursorobj.execute(query)
                result = cursorobj.fetchall()
                if not read:
                    connection.commit()
        except Exception, e:
                print "Err", e
        connection.close()
        return result

def getProjects():
    return _sql("SELECT id, project_name, project_fullname, project_url, project_description, project_long_description FROM MLABvo.vo_projects;", read = True)

def getProjectByName(name):
    return _sql("SELECT id, project_name, project_fullname, project_url, project_description, project_long_description FROM MLABvo.vo_projects WHERE project_name = '%s';" %(name), read = True)

def getProjectTables(name):
    return _sql("SELECT id, schema_name, table_name, table_type, utype, description, table_index, id_project FROM MLABvo.tables WHERE id_project = (SELECT id FROM MLABvo.vo_projects WHERE project_name = '%s');" %(name), read = True)


def index(request):
    #latest_question_list = VoFileindex.objects.order_by('id')[:5]
    #obs = get_object_or_404(VoFileindex, pk=2)
    obs = VoFileindex.objects
    
    return HttpResponse( "...." + repr(obs)+ "----" + repr(AuthUser) )
    #return render(request, 'multibolid/index.html', context)


def home():
    #latest_question_list = VoFileindex.objects.order_by('id')[:5]
    obs = get_object_or_404(VoFileindex, pk=2)
    context = {'obs': obs}
    print context
    return render(request, 'multibolid/index.html', context)

