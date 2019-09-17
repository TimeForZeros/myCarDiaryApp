from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
import uuid
import boto3
from .models import Car, Features, Maintenance
from .forms import MaintenanceForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'mycardiary'


# Create your views here.

class CarCreate(CreateView):
  model = Car
  fields = ['make', 'model', 'year', 'color', 'transmission',
             'seats', 'engine', 'odometer', 'state_reg', 'title']

class CarUpdate(UpdateView):
  model = Car
  fields = ['color', 'odometer', 'state_reg', 'title']

class CarDelete(DeleteView):
  model = Car
  success_url = '/cars/'



def home(request):
    return render(request, 'home.html')

def cars_index(request):
  cars = Car.objects.all()
  return render(request, 'cars/index.html', { 'cars': cars })

def cars_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    maintenance_form = MaintenanceForm()
    # feature = Features.objects.all()
    return render(request, 'cars/detail.html', {
        'car': car,
        'maintenance_form': maintenance_form,
        # 'feature': feature,
    })

def add_maintenance(request, car_id):
    form = MaintenanceForm(request.POST)
    if form.is_valid():
        new_maintenance = form.save(commit=False)
        new_maintenance.car_id = car_id
        new_maintenance.save()
    return redirect ('detail', car_id=car_id)

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)




##############  When upload photo functionality works ###############

def add_photo(request, car_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.clients('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.')
    ]