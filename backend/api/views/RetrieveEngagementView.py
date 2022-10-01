from django.shortcuts import render
from rest_framework import generics, status
from ..models import User
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class RetrieveEngagementView(APIView):
    def get(self, request):
        name = request.query_params.get('name')
        course = request.query_params.get('course')
        module = request.query_params.get('module')
        group = request.query_params.get('group')
        queryList = User.queryEngagedStatus(course, group, module, name)
        payload = {"engaged_status": queryList}
        return Response(payload)
