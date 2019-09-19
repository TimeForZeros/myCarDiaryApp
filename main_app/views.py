from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
import uuid
import boto3
from .models import Car, Features, Maintenance, Photo
from .forms import MaintenanceForm

S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'mycardiary'

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

class CarCreate(CreateView):
  model = Car
  fields = ['make', 'model', 'year', 'color', 'transmission',
             'seats', 'engine', 'odometer', 'state_reg', 'title']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

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
@login_required
def cars_index(request):
  cars = Car.objects.filter(user=request.user)
  return render(request, 'cars/index.html', { 'cars': cars })
#   return render(request, 'cars/index.html', { 'cars': cars })

@login_required
def cars_detail(request, car_id):
    car = Car.objects.get(id=car_id)
    maintenance_form = MaintenanceForm()
    features = Features.objects.all()
    return render(request, 'cars/detail.html', {
        'car': car,
        'maintenance_form': maintenance_form,
        'features': features,
    })
@login_required
def add_maintenance(request, car_id):
    form = MaintenanceForm(request.POST)
    if form.is_valid():
        new_maintenance = form.save(commit=False)
        new_maintenance.car_id = car_id
        new_maintenance.save()
    return redirect ('detail.html', car_id=car_id)


@login_required
def add_photo(request, car_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            photo = Photo(url=url, car_id=car_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', car_id=car_id)




class MaintenanceList(LoginRequiredMixin, ListView):
  model = Maintenance

class MaintenanceDetail(LoginRequiredMixin, DetailView):
  model = Maintenance

class MaintenanceCreate(LoginRequiredMixin, CreateView):
  model = Maintenance
  fields = '__all__'

   
class MaintenanceUpdate(LoginRequiredMixin, UpdateView):
  model = Maintenance
  fields = '__all__'

class MaintenanceDelete(LoginRequiredMixin, DeleteView):
  model = Maintenance
  success_url = '/maintenance/'



@login_required
def assoc_feature(request, car_id, feature_id):
  Car.objects.get(id=car_id).features.add(feature_id)
  return redirect('detail', car_id=car_id)

@login_required
def unassoc_feature(request, car_id, feature_id):
  Car.objects.get(id=car_id).features.remove(feature_id)
  return redirect('detail', car_id=car_id)


class FeaturesList(LoginRequiredMixin, ListView):
  model = Features

class FeaturesDetail(LoginRequiredMixin, DetailView):
  model = Features

class FeaturesCreate(LoginRequiredMixin, CreateView):
  model = Features
  fields = '__all__'

class FeaturesUpdate(LoginRequiredMixin, UpdateView):
  model = Features
  fields = ['wishlist']

class FeaturesDelete(LoginRequiredMixin, DeleteView):
  model = Features
  success_url = '/features/'

