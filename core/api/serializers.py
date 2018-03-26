from rest_framework import serializers

from core.models import GeoPosition, WeatherRecord, WeatherSummary


class GeoPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = GeoPosition
        fields = '__all__'


class WeatherRecordSerializer(serializers.ModelSerializer):
    geo_position = GeoPositionSerializer()

    class Meta:
        model = WeatherRecord
        fields = '__all__'


class WeatherSummarySerializer(serializers.ModelSerializer):
    geo_position = GeoPositionSerializer()

    class Meta:
        model = WeatherSummary
        fields = '__all__'
