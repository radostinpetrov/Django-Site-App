# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import requests
from django.shortcuts import render, redirect
from .models import TodoList, Category, City
from .forms import CityForm


def index(request):
    todos = TodoList.objects.all()
    categories = Category.objects.all()
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric'  # API url

    if request.method == 'POST':  # checking if the request method is a POST
        form = CityForm(requests.post)

        if 'taskAdd' in request.POST:
            title = request.POST['description']
            date = str(request.POST['date'])
            category = request.POST['category_select']
            content = title + ' -- ' + date + ' ' + category
            Todo = TodoList(title=title, content=content, due_date=date, category=Category.objects.get(name=category))
            Todo.save()
            return redirect("/")  # reloading the page

        if 'taskDelete' in request.POST:
            checkedlist = request.POST['checkedbox']
            for todo_id in checkedlist:
                todo = TodoList.objects.get(id=int(todo_id))
                todo.delete()

    form = CityForm()
    weather_data = []
    city = City(name='London')

    r = requests.get(url.format(city)).json()

    city_weather = {
        'city': city.name,
        'temperature': r['main']['temp'],
        'description': r['weather'][0]['description'],
        'icon': r['weather'][0]['icon'],
    }

    weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'index.html', {'todos': todos, 'categories': categories}, context)
