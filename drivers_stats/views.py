from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from drivers_stats.serializer import DriverSerializer
from drivers_stats.models import Drivers


class DriverViewSet(ModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer
    filter_backends = [filters.OrderingFilter]
    ordering = ('-season_points',)
    http_method_names = ['get']

