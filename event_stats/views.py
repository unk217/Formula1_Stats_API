from rest_framework import viewsets
from event_stats.serializer import EventSerializer
from event_stats.models import Event

# Create your views here.
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    http_method_names = ['get']
# This viewset provides the default `list`, `create`, `retrieve`, `update`, and `destroy` actions.
