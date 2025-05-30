from rest_framework import serializers
from drivers_stats.models import Drivers

class DriverSerializer(serializers.ModelSerializer):
    class Meta:
        model = Drivers
        fields = '__all__'