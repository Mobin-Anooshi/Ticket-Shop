from rest_framework import serializers
from .models import Travel,TravelDetails


class TravelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travel
        fields = (
            'origin',
            'destination',
            'departure_time',
            'available_seats',
        )
class TravelDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelDetails
        fields = (
            'price',
            'vehicle_id',
            'driver_id',
            'distance'
        )
