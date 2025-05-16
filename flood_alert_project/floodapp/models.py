from django.db import models

class FloodDataRecord(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    average_rainfall = models.FloatField()
    temperature = models.FloatField()
    humidity = models.FloatField()
    flood_occurred = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

class LocationSubmission(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.latitude}, {self.longitude} @ {self.timestamp}"
    class HistoricalRainfall(models.Model):
     location_name = models.CharField(max_length=100)
     date = models.DateField()
     rainfall_mm = models.FloatField()

     def __str__(self):
        return f"{self.location_name} - {self.date} - {self.rainfall_mm}mm"