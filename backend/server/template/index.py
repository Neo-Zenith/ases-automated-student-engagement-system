from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.template import loader
from api.models import User

def index(request):
    template = loader.get_template('./views/index.html')
    return HttpResponse(template.render())

def returngraph(request):
    course = request.POST["course"]
    module = request.POST["module"]
    group = request.POST["group"]

    if group:
        group = int(group)
    # status = User.queryGroupEngagedStatus(course, group, module)
    status = User.queryGroupEngagedStatus(course, group, module)

    return render(request, "./views/ReturnGraph.html", {'status': status})