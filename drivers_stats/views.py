from rest_framework import viewsets
from drivers_stats.serializer import DriverSerializer
from drivers_stats.models import Drivers

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer


