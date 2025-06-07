from rest_framework.viewsets import ReadOnlyModelViewSet
from drivers_stats.serializer import DriverSerializer
from drivers_stats.models import Drivers


class DriverViewSet(ReadOnlyModelViewSet):
    queryset = Drivers.objects.all()
    serializer_class = DriverSerializer


