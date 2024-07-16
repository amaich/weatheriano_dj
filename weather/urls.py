from django.urls import path
from .views import *


app_name = 'weather'

urlpatterns = [
    path('', index, name='index'),
    path('search/', city_search, name='city_search')
]