from django.db import models


# Модель для хранения количества запросов по каждому городу
class CityModel(models.Model):
    name = models.CharField(max_length=100)
    search_count = models.IntegerField()
