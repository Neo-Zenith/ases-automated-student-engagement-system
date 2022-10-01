from django.shortcuts import render
from rest_framework import generics, status
from ..models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import EngagementViewSerializer

# Create your views here.
class GetEngagementView(APIView):
    def get(self, request):
        course = request.query_params.get('course')
        queryList = User.queryEngagedStatus(course)
        payload = {"engaged_status": queryList}
        return Response(payload)
