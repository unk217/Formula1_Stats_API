from rest_framework.viewsets import ModelViewSet
from teams_stats.serializer import TeamSerializer
from teams_stats.models import Team
class TeamViewSet(ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    http_method_names = ['get']

