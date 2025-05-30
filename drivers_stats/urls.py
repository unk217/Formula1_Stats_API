from django.urls import path, include
from rest_framework import routers
from .views import DriverViewSet

routers = routers.DefaultRouter()
routers.register(r'', DriverViewSet, basename='driver')
urlpatterns = [
    path('', include(routers.urls)),
]