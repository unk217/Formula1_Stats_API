from django.urls import path, include
from rest_framework import routers
from .views import TeamViewSet

routers = routers.DefaultRouter()
routers.register(r'', TeamViewSet, basename='teams')

urlpatterns = routers.urls