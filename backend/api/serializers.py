from rest_framework import serializers
from .models import User

class EngagementViewSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ['name', 'course', 'engaged_status', 'time', 'fps', 'module', 'group', 'matric_id']
        