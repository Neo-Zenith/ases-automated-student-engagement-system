from unittest.util import _MAX_LENGTH
from django.db import models

# Create your models here.
class User (models.Model):
    name = models.CharField(max_length=50)
    module = models.CharField(max_length=50)
    group = models.IntegerField()
    email = models.CharField(max_length=100)
    course = models.CharField(max_length=50)
    gender = models.BooleanField(null=False)
    engaged_status = models.CharField(max_length=1000000)
    time = models.CharField(max_length=100000)
    fps = models.CharField(max_length=1000)

    def register(self):
        self.save()

    @staticmethod
    def queryEngagedStatus(course, group, module, name):
        mega_list = []
        query_set = User.objects.filter(course=course, group=int(group), module=module, name=name)
        for i in query_set:
            mega_list.append(i.engaged_status.strip('][').split(', '))

        return mega_list
    

