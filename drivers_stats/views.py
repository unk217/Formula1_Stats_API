from rest_framework.viewsets import ModelViewSet
from drivers_stats.serializer import DriverSerializer
from drivers_stats.models import Drivers


class DriverViewSet(ModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer
    http_method_names = ['get']


