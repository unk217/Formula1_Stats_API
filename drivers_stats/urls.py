from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import routers
from .views import DriverViewSet

routers = routers.DefaultRouter()
routers.register(r'', DriverViewSet, basename='driver')

@api_view (['GET'])
def api_root(request, format=None):
    return Response({
        'drivers': reverse('driver-list', request=request, format=format),
    })

urlpatterns = [
    #path('', api_root, name='api-root'),
    path('', include(routers.urls)),
]