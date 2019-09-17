from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
import uuid
import boto3
from .models import Car, Features, Maintenance
# from .forms import MaintenanceForm


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
    return HttpResponse('Test')

def cars_index(request):
  cars = Car.objects.all()
  return render(request, 'cars/index.html', { 'cars': cars })

def cars_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    maintenance_form = MaintenanceForm()
    feature = Features.objects.all()
    return render(request, 'cars/detail.hmtl', {
        'car': car,
        'maintenance_form': maintenance_form,
        'feature': feature,
    })

def add_maintenance(request, car_id):
    form = MaintenanceForm(request.POST)
    if form.is_valid():
        new_maintenance = form.save(commit=False)
        new_maintenance.car_id = car_id
        new_maintenance.save()
    return redirect ('detail', car_id=car_id)




##############  When upload photo functionality works ###############

# def add_photo(request, car_id):
#     photo_file = request.FILES.get('photo-file', None)
#     if photo_file:
#         s3 = boto3.clients('s3')
#         key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.')
#         try:
#             s3.upload_fileobj(photo_file, BUCKET, key)
#             url = f'{S3_BASE_URL}{BUCKET}/{key}'
#             photo = Photo(url=url, car_id=car_id)
#             photo.save()
#         except:
#             print('An error occurred uploading file to S3')
#         return redirect('detail', car_id=car_id)
#         ]