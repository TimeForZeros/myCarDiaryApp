
# Generated by Django 2.2.3 on 2019-09-17 22:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('year', models.IntegerField()),
                ('color', models.CharField(max_length=50)),
                ('transmission', models.CharField(max_length=100)),
                ('seats', models.IntegerField()),
                ('engine', models.CharField(max_length=100)),
                ('odometer', models.IntegerField()),
                ('state_reg', models.TextField(max_length=2)),
                ('title', models.TextField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Features',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=50)),
                ('wishlist', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='maintenance date')),
                ('odo_reading', models.IntegerField()),
                ('task', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=50)),
                ('notes', models.CharField(max_length=250)),
                ('price', models.IntegerField()),
                ('to_do', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Car')),
            ],
        ),
    ]
