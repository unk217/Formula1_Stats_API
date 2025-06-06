from rest_framework import serializers
from drivers_stats.models import Drivers

class DriverSerializer(serializers.ModelSerializer):
    age = serializers.ReadOnlyField(source='driver_age')
    class Meta:
        model = Drivers
        fields = (
            'id',
            'driver',
            'driver_number',
            'team',
            'country',
            'podiums',
            'season_points',
            'total_points',
            'gp_entered',
            'world_championships',
            'highest_race_finish',
            'highest_grid_position',
            'date_birth',
            'age',
            'place_birth',
            )