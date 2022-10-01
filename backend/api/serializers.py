from rest_framework import serializers
from .models import User

class EngagementViewSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'course', 'gender', 'engaged_status', 'time', 'fps']
        