from django.contrib import admin
from django.urls import path, include

from .views.GetEngagementView import GetEngagementView
from .views.EngagementView import EngagementView

urlpatterns = [
    path("engagement", EngagementView.as_view()),
    path("engagement/get", GetEngagementView.as_view())
]