from django.db import models
from django.dispatch import receiver


class GeoPosition(models.Model):
    # For the sake of simplicity assume that all coordinates are integers
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    elevation = models.IntegerField()

    def __str__(self):
        return '(%d, %d, %d)' % (self.latitude, self.longitude, self.elevation)


class WeatherRecord(models.Model):
    geo_position = models.ForeignKey(GeoPosition, related_name='weather_records')

    date = models.DateField()
    time = models.TimeField()
    temperature = models.FloatField()
    wind_speed = models.FloatField()
    wind_direction = models.FloatField()

    processed = models.BooleanField(default=False)


class WeatherSummary(models.Model):
    geo_position = models.OneToOneField(GeoPosition, related_name='weather_summary')

    average_temperature = models.FloatField(null=True, blank=True, default=None)
    average_wind_speed = models.FloatField(null=True, blank=True, default=None)
    average_wind_direction = models.FloatField(null=True, blank=True, default=None)

    records_count = models.IntegerField(default=0)


@receiver(models.signals.post_save, sender=GeoPosition)
def initialize_weather_summary(sender, instance, created, **kwargs):
    if created:
        WeatherSummary.objects.create(geo_position=instance)
