from django.shortcuts import render
from rest_framework import generics, status
from ..models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from ..serializers import EngagementViewSerializer

# Create your views here.
class EngagementView(APIView):
    serializer_class = EngagementViewSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            name = request.data.get('name')
            email = request.data.get('email')
            course = request.data.get('course')
            gender = request.data.get('gender')
            engaged_status = request.data.get('engaged_status')
            time = request.data.get('time')
            fps = request.data.get('fps')

            user = User(name=name, email=email, course=course, engaged_status=engaged_status, gender=gender, time=time, fps=fps)
            user.register()
            print(User.queryEngagedStatus(course="CSC/2"))
            payload = {"error": "OK"}
            return Response(payload)