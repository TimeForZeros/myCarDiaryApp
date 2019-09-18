from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import boto3
import uuid
from .models import Car, Features, Maintenance, Photo
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

# def cars_index(request):
#   cars = Car.objects.all()
#   return render(request, 'cars/index.html', { 'cars': cars })
@login_required
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

@login_required
def cars_index(request):
  cars = Car.objects.filter(user=request.user)
  return render(request, 'cars/index.html', { 'cars': cars })

# def cars_detail(request, cat_id):
#   car = Car.objects.get(id=car_id)
#   # Get the toys the cat doesn't have
#   return render(request, 'cats/detail.html', {
#     # Pass the cat and feeding_form as context
#     'car': car, 
#     # 'maintenance_form': maintenance_form,

  # })




##############  When upload photo functionality works ###############

def add_photo(request, car_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to cat_id or cat (if you have a cat object)
            photo = Photo(url=url, car_id=car_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', car_id=car_id) # look closely at this particular line of code