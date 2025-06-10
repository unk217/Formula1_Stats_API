from django.urls import path, include
from rest_framework import routers
from .views import EventViewSet

routers = routers.DefaultRouter()
routers.register(r'', EventViewSet, basename='events')
urlpatterns = routers.urls
