from django.forms import ModelForm
from .models import Maintenance, Features, Car, Photo

class CarForm(ModelForm):
  class Meta:
    model = Car
    fields = ['make', 'model', 'year', 'color', 'transmission', 'seats', 'engine', 'odometer', 'state_reg', 'title']

class MaintenanceForm(ModelForm):
  class Meta:
    model = Maintenance
    fields = ['date', 'odo_reading', 'task', 'location', 'notes', 'price']

class FeaturesForm(ModelForm):
  class Meta:
    model = Features
    fields = ['feature', 'wishlist']