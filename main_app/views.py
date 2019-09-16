from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Car


# Create your views here.
def home(request):
    return HttpResponse('Test')

def cars_index(request):
    cars = Car.objects.all()
    return render(request, 'cars/index.html', {'cars': cars})

def cars_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    maintenance_form = MaintenanceForm()
    features_form = FeaturesForm()
    return render(request, 'cars/detail.html', {
        'car': car, 
        'maintenance_form': maintenance_form,
        'features_form': features_form,
    })