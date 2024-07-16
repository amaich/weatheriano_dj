from django.shortcuts import render
from django.http import HttpResponse

import requests


def get_coords(city: str) -> dict | None:
    response = requests.get('https://geocoding-api.open-meteo.com/v1/search',
                          params={"name": city})
    if 'results' in response.json():
        latitude = str(response.json()['results'][0]['latitude'])
        longitude = str(response.json()['results'][0]['longitude'])

        return {'latitude': latitude, 'longitude': longitude}
    else:
        return None


def get_weather_for_city_by_hours(city: str, hours: int) -> requests.models.Response | None:
    coords = get_coords(city)
    if coords:
        weather_resp = requests.get('https://api.open-meteo.com/v1/forecast',
                                    params={'latitude': coords['latitude'],
                                            'longitude': coords['longitude'],
                                            'hourly': ["temperature_2m", "rain", "cloud_cover", "weather_code"],
                                            'forecast_days': 1,
                                            'forecast_hours': hours})

        return weather_resp
    else:
        return None


def get_weather_for_city_by_days(city, days)  -> requests.models.Response | None:
    coords = get_coords(city)
    if coords:
        weather_resp = requests.get('https://api.open-meteo.com/v1/forecast',
                                    params={'latitude': coords['latitude'],
                                            'longitude': coords['longitude'],
                                            'hourly': ["temperature_2m", "rain", "cloud_cover", "weather_code"],
                                            'forecast_days': days})

        return weather_resp
    else:
        return None


def index(request):
    return render(request, 'weather/index.html', context={})


def city_search(request):

    r = get_weather_for_city_by_hours(request.GET['city'], 6)

    return HttpResponse(r)
