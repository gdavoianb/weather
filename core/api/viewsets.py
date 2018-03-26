from rest_framework.viewsets import ModelViewSet

from core.api.serializers import (
    GeoPositionSerializer, WeatherRecordSerializer, WeatherSummarySerializer
)
from core.models import GeoPosition, WeatherRecord, WeatherSummary


class GeoPositionAPI(ModelViewSet):
    queryset = GeoPosition.objects.all()
    serializer_class = GeoPositionSerializer


class WeatherRecordAPI(ModelViewSet):
    queryset = WeatherRecord.objects.all()
    serializer_class = WeatherRecordSerializer


class WeatherSummaryAPI(ModelViewSet):
    queryset = WeatherSummary.objects.all()
    serializer_class = WeatherSummarySerializer
