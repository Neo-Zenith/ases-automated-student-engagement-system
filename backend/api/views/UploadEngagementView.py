from django.shortcuts import render
from rest_framework import generics, status
from ..models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import EngagementViewSerializer

# Create your views here.
class UploadEngagementView(APIView):
    serializer_class = EngagementViewSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = request.data.get('name')
            course = request.data.get('course')
            engaged_status = request.data.get('engaged_status')
            time = request.data.get('time')
            fps = request.data.get('fps')
            module = request.data.get('module')
            group = request.data.get('group')

            user = User(name=name, course=course, engaged_status=engaged_status, time=time, fps=fps, module=module, group=group)
            user.register()
            payload = {"error": "OK"}
            return Response(payload)