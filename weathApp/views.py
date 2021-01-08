from django.shortcuts import render, redirect
import requests
from .models import City
from .forms  import CityForm

# Create your views here.
def index(request):
    url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0487c8fa4d3b5567e594bfbbe3fd96e0"
    err = ''
    message = ''
    message_class = ''
    if request.method == 'POST':
        form = CityForm(request.POST)

        if form.is_valid():
            new_city = form.cleaned_data['name']
            city_count = City.objects.filter(name=new_city).count()
            if city_count == 0:
                r = requests.get(url.format(new_city)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    err = 'City not exist'
            else:
                err = 'Already exist'

        if err:
            message = err
            message_class = 'alert-danger'
        else:
            message = 'City added'
            message_class = 'alert-success'    
   
    form = CityForm()

    weather_data = []
    cities = City.objects.all()


    try:
        for city in cities:
            r = requests.get(url.format(city)).json()

            city_weather = {
            'city' : city.name,
            'temperature' : r['main']['temp'],
            'description' : r['weather'][0]['description'],
            'icon' : r['weather'][0]['icon'],
            }

            weather_data.append(city_weather)
    except KeyError:
        pass
    except EXCEPTION as e:
        pass

    context = {
        'weather_data' : weather_data,
        'form' : form,
        'message' : message,
        'message_class' : message_class,
    }


    return render(request, 'weathApp/index.html', context)

def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()
    return redirect('index')