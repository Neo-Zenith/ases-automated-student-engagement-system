from django.contrib import admin
from django.urls import path, include

from .views.RetrieveEngagementView import RetrieveEngagementView
from .views.UploadEngagementView import UploadEngagementView

urlpatterns = [
    path("v1/engagement/upload", UploadEngagementView.as_view()),
    path("v1/engagement/retrieve", RetrieveEngagementView.as_view())
]