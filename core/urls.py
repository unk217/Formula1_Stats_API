from rest_framework.routers import DefaultRouter
from django.urls import path, include

from drivers_stats.views import DriverViewSet
from event_stats.views import EventViewSet
from core.views import APIRootView

# Create your views here.
router = DefaultRouter()
router.register(r'drivers', DriverViewSet, basename='drivers')
router.register(r'events', EventViewSet, basename='events')

urlpatterns = [
    path("", APIRootView.as_view(), name="api-root"),
    path('drivers/', include('drivers_stats.urls')),
    path('events/', include('event_stats.urls')),
    #path('', include(router.urls)),
]