from rest_framework import serializers
from teams_stats.models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = (
            'id',
            'name',
            'full_name',
            'points',
            'base',
            'team_principal',
            'chassis',
            'power_unit',
            'first_entry',
            'world_championships',
            'highest_race_finish',
            'pole_positions',
            'fastest_laps',
            ) 