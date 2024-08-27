import requests
from django.core.cache import cache
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings


def fetch_updated_weather_data(city: str):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}"

    params = {
        'unitGroup': 'metric',
        'key': settings.API_KEY,
        'contentType': 'json'
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        return data, response.status_code
    except requests.exceptions.RequestException as e:
        return False, e


class WeatherDataView(APIView):
    def get(self, request):
        location = request.query_params.get('city', '')
        cache_key = f'weather_data_for_{location}'
        data = cache.get(cache_key)

        if not location:
            return Response({"detail": "No city provided,\nUse  http://localhost:8000/?city='Kampala'", },
                            status=status.HTTP_400_BAD_REQUEST)

        if not data:
            data, error = fetch_updated_weather_data(location)
            cache.set(cache_key, data, settings.CACHE_TIMEOUT)

        return Response(data={f"{location}": data}, status=status.HTTP_200_OK)
