from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.template import loader
from api.models import User
import json

def index(request):
    template = loader.get_template('./views/index.html')
    return HttpResponse(template.render())

def returngraph(request):
    course = request.POST["course"]
    module = request.POST["module"]
    group = request.POST["group"]
    matric_id = request.POST["matric_id"]

    if matric_id != "":      
        status = User.queryEngagedStatus(course, group, module, matric_id)
    else:
        status = User.queryGroupEngagedStatus(course, group, module)
        print(status)

    if group:
        group = int(group)
    
    listOfEngagedStatus = []
    for i in status.values():
        listOfEngagedStatus.append(i['engaged_status'])
    
    group_status = {}
    try:
        group_status['matric_id'] = status[0]['matric_id']
    except:
        pass

    group_status['module'] = module
    group_status['group'] = group
    group_status['engaged_status'] = User.getSumEngagedStatus(listOfEngagedStatus)
    group_status['duration'] = len(User.getSumEngagedStatus(listOfEngagedStatus))
     
    payload = {
        'error': "OK",
        'group_status': group_status,
    }
    return render(request, "./views/ReturnGraph.html", payload)
