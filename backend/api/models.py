from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class UserManager(models.Manager):
    def queryFilter(self, **filters):
        filters = {k:v for k,v in filters.items() if v is not None}
        qs = self.get_queryset()
        return qs.filter(**filters)

class User (models.Model):
    objects = UserManager()
    name = models.CharField(max_length=50)
    module = models.CharField(max_length=50)
    group = models.IntegerField()
    course = models.CharField(max_length=50)
    engaged_status = models.CharField(max_length=1000000)
    time = models.IntegerField()
    fps = models.CharField(max_length=1000)
    session = models.DateTimeField(auto_now=True)

    def register(self):
        self.save()

    @staticmethod
    def queryEngagedStatus(course, group, module, name):
        mega_list = {}

        query_set = User.objects.queryFilter(course=course, group=group, module=module, name=name)
        id = 0
        for i in query_set:
            mega_list[id] = {}
            mega_list[id]['name'] = i.name
            mega_list[id]['course'] = i.course
            mega_list[id]['module'] = i.module
            mega_list[id]['group'] = i.group
            converted_engaged_status = User.flattenFrames(i.engaged_status.strip('][').split(', '), i.fps)
            mega_list[id]['engaged_status'] = converted_engaged_status
            mega_list[id]['duration'] = i.time
            mega_list[id]['session'] = i.session
            id += 1
            

        return mega_list
    
    def queryGroupEngagedStatus(course, group, module):
        mega_list = {}

        query_set = User.objects.queryFilter(course=course, group=group, module=module)
        id = 0
        for i in query_set:
            mega_list[id] = {}
            mega_list[id]['course'] = i.course
            mega_list[id]['module'] = i.module
            mega_list[id]['group'] = i.group
            converted_engaged_status = User.flattenFrames(i.engaged_status.strip('][').split(', '), i.fps)
            mega_list[id]['engaged_status'] = converted_engaged_status
            mega_list[id]['duration'] = i.time
            mega_list[id]['session'] = i.session
            id += 1
        return mega_list

    @staticmethod
    def flattenFrames(data, fps): #input: data of frames, fps; output: engagement score in seconds
        dict = {'Time':[], 'Status':[]}
        times = 1/float(fps)
        
        for i in range(1, len(data)+1):
            dict['Time'].append(times*i)
            dict['Status'].append(data[i-1])
        
        engagementscore = []
        second = 1
        counter = 0
        statuscount = 0
        
        for i in range(0, len(dict['Time'])):
            print(engagementscore)
            if dict['Time'][i] < second: 
                counter += 1
                if dict['Status'][i] == '1':
                    statuscount += 1
            else:
                if statuscount > counter/2:
                    engagementscore.append(1)
                else:
                    engagementscore.append(0)
                second += 1
                counter = 0
                statuscount = 0
        
        return engagementscore
