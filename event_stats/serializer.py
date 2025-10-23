from rest_framework import serializers
from event_stats.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'id',
            "round",
            'event',
            'country',
            'circuit',
            'city',
            'date',
            'first_gp',
            'number_laps',
            'circuit_lenght',
            'race_distance',
            'lap_record',
            )
