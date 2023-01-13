import requests
from django.shortcuts import render


def index(request):
    appid = '6d4ae3e6017b173e07004a351a2ab700'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + appid

    city = 'Zakopane'
    res = requests.get(url.format(city)).json()

    city_info = {
        'city': city,
        'temp': res["main"]["temp"],
        'humidity': res["main"]["humidity"],
        'icon': res["weather"][0]["icon"],
        'wind': res["wind"]["speed"]
    }

    context = {'info': city_info}
    return render(request, 'weather/index.html', context)
