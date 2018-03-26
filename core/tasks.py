from collections import defaultdict

from celery import shared_task
from django.conf import settings
from django.core.cache import cache

from core.models import GeoPosition, WeatherRecord


def build_weather_statistics_report():
    geo_positions = GeoPosition.objects.select_related(
        'weather_summary'
    ).order_by('latitude', 'longitude', 'elevation')

    payload = [('Latitude', 'Longitude', 'Elevation',
                'Records Count', 'Average Temperature',
                'Average Wind Speed', 'Average Wind Direction')]

    for geo_position in geo_positions:
        weather_summary = geo_position.weather_summary
        payload.append(
            (geo_position.latitude, geo_position.longitude, geo_position.elevation,
             weather_summary.records_count, weather_summary.average_temperature,
             weather_summary.average_wind_speed, weather_summary.average_wind_direction)
        )

    cache.set(settings.UPDATE_WEATHER_STATISTICS_CACHE_KEY, payload,
              timeout=settings.UPDATE_WEATHER_STATISTICS_TASK_PERIOD)

    return payload


@shared_task
def update_weather_statistics():
    weather_records_to_process = WeatherRecord.objects.select_related(
        'geo_position__weather_summary'
    ).filter(processed=False)

    weather_records_by_geo_positions = defaultdict(list)
    for weather_record in weather_records_to_process:
        geo_position = weather_record.geo_position
        weather_records_by_geo_positions[geo_position].append(weather_record)

    for geo_position, weather_records in weather_records_by_geo_positions.items():
        weather_summary = geo_position.weather_summary

        old_records_count = weather_summary.records_count
        new_records_count = old_records_count + len(weather_records)

        # Handle possible None values

        old_temperatures_sum = (weather_summary.average_temperature or 0) * old_records_count
        new_temperatures_sum = old_temperatures_sum + sum(
            weather_record.temperature for weather_record in weather_records
        )

        old_wind_speeds_sum = (weather_summary.average_wind_speed or 0) * old_records_count
        new_wind_speeds_sum = old_wind_speeds_sum + sum(
            weather_record.wind_speed for weather_record in weather_records
        )

        old_wind_directions_sum = (weather_summary.average_wind_direction or 0) * old_records_count
        new_wind_directions_sum = old_wind_directions_sum + sum(
            weather_record.wind_direction for weather_record in weather_records
        )

        weather_summary.average_temperature = new_temperatures_sum / new_records_count
        weather_summary.average_wind_speed = new_wind_speeds_sum / new_records_count
        weather_summary.average_wind_direction = new_wind_directions_sum / new_records_count

        weather_summary.records_count = new_records_count

        weather_summary.save()

    weather_records_to_process.update(processed=True)

    # Cache the latest report
    build_weather_statistics_report()
