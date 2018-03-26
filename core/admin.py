from django.contrib import admin

from core.models import GeoPosition, WeatherRecord, WeatherSummary


@admin.register(GeoPosition)
class GeoPositionAdmin(admin.ModelAdmin):
    list_display = ['id', 'latitude', 'longitude', 'elevation']


@admin.register(WeatherRecord)
class WeatherRecordAdmin(admin.ModelAdmin):
    list_display = ['id', 'geo_position', 'processed']


@admin.register(WeatherSummary)
class WeatherSummaryAdmin(admin.ModelAdmin):
    list_display = ['id', 'geo_position', 'records_count']
