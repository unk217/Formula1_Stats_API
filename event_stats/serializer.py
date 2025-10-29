from rest_framework import serializers

class LocationSerializer(serializers.Serializer):
    locality = serializers.CharField()
    country = serializers.CharField()


class CircuitSerializer(serializers.Serializer):
    circuit_id = serializers.CharField(source='circuitId')
    name = serializers.CharField(source='circuitName')
    location = LocationSerializer(source='Location')


class SessionSerializer(serializers.Serializer):
    date = serializers.DateField(required=False, allow_null=True)
    time = serializers.TimeField(required=False, allow_null=True)

class RaceSerializer(serializers.Serializer):
    round = serializers.CharField()
    season = serializers.CharField()
    name = serializers.CharField(source='raceName')
    date = serializers.DateField()
    time = serializers.TimeField()
    circuit = CircuitSerializer(source='Circuit')
    FirstPractice = SessionSerializer(required=False)
    SecondPractice = SessionSerializer(required=False)
    ThirdPractice = SessionSerializer(required=False)  
    SprintQualifying = SessionSerializer(required=False)
    Sprint = SessionSerializer(required=False)
    Qualifying = SessionSerializer(required=False)

