from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy

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


def weather_search(request):
    if request.GET.get('search_type') == 'by_hours':
        weather = get_weather_for_city_by_hours(request.GET.get('city'), 6)
    elif request.GET.get('search_type') == 'by_days':
        weather = get_weather_for_city_by_days(request.GET.get('city'), 6)
    else:
        return render(request, 'weather/weather_search.html', context={'error': 'choose search type'})

    if weather:
        return render(request, 'weather/weather_search.html', context={'weather': weather.json()})
    else:
        return render(request, 'weather/weather_search.html', context={'error': 'city name error'})
