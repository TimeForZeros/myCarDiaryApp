from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User


######CLASS MODELS#########
class Features(models.Model):
    feature = models.CharField(max_length=50)
    wishlist = models.BooleanField(default=True)

    def __str__(self):
        return self.feature
    def get_absolute_url(self):
        return reverse('feature_detail', kwargs={'pk': self.id})

class Car(models.Model):
    make = models.CharField(
        max_length=100,
        default='Ford')
    model = models.CharField(
        max_length=100,
        default='Model T')
    year = models.IntegerField(
        default=1925
    )
    color = models.CharField(
        max_length=50,
        default='Black'
    )
    transmission = models.CharField(
        max_length=100,
        default='Automatic')
    seats = models.IntegerField(
        default=0
    )
    engine = models.CharField(
        max_length=100,
        default='V8'
        )
    odometer = models.IntegerField(
        default=42069,
    )
    state_reg = models.TextField(
        max_length=2,
        default='CA'
        )
    title = models.TextField(
        max_length=100,
        default='Clean'
        )
    features = models.ManyToManyField(Features)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.model

    def get_absolute_url(self):
        return reverse('detail', kwargs={'car_id': self.id})


class Maintenance(models.Model):
    date = models.DateField('maintenance date')
    odo_reading = models.IntegerField()
    new_oil = models.IntegerField()
    task = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    notes = models.CharField(max_length=250)
    price = models.IntegerField()

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
   

    def __str__(self):
        return f'{self.task} on {self.date}'

class Photo(models.Model):
    url = models.CharField(max_length=200)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for car_id: {self.car_id} @{self.url}"