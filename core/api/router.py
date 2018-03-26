from rest_framework import routers

from core.api.viewsets import GeoPositionAPI, WeatherRecordAPI, WeatherSummaryAPI


router = routers.DefaultRouter()

router.register('geo_position', GeoPositionAPI)
router.register('weather_record', WeatherRecordAPI)
router.register('weather_summary', WeatherSummaryAPI)
