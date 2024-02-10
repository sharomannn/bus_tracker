# Generated by Django 5.0.1 on 2024-02-10 09:05

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, unique=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='bus_images/', verbose_name='Изображение автобуса')),
            ],
            options={
                'verbose_name': 'Автобус',
                'verbose_name_plural': 'Автобусы',
            },
        ),
        migrations.CreateModel(
            name='CarNumber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10, unique=True)),
            ],
            options={
                'verbose_name': 'Номер машины',
                'verbose_name_plural': 'Номера машин',
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Имя водителя')),
            ],
            options={
                'verbose_name': 'Водитель',
                'verbose_name_plural': 'Водители',
            },
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название маршрута')),
            ],
            options={
                'verbose_name': 'Маршрут',
                'verbose_name_plural': 'Маршруты',
            },
        ),
        migrations.CreateModel(
            name='BusProxy',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('bus.bus',),
        ),
        migrations.CreateModel(
            name='BusStop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='Название остановки')),
                ('latitude', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(-90), django.core.validators.MaxValueValidator(90)], verbose_name='Широта')),
                ('longitude', models.FloatField(blank=True, validators=[django.core.validators.MinValueValidator(-180), django.core.validators.MaxValueValidator(180)], verbose_name='Долгота')),
                ('nearby_stops', models.ManyToManyField(blank=True, to='bus.busstop')),
            ],
            options={
                'verbose_name': 'Остановка',
                'verbose_name_plural': 'Остановки',
            },
        ),
        migrations.AddField(
            model_name='bus',
            name='car_number',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.carnumber', verbose_name='Номер машины'),
        ),
        migrations.CreateModel(
            name='BusDriver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.bus', verbose_name='Автобус')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.driver', verbose_name='Водитель')),
            ],
            options={
                'verbose_name': 'Водитель автобуса',
                'verbose_name_plural': 'Водители автобусов',
            },
        ),
        migrations.AddField(
            model_name='bus',
            name='driver',
            field=models.ManyToManyField(through='bus.BusDriver', to='bus.driver', verbose_name='Водители'),
        ),
        migrations.CreateModel(
            name='RouteBusStop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(verbose_name='Порядок следования')),
                ('bus_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.busstop', verbose_name='Остановка')),
                ('route', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.route', verbose_name='Маршрут')),
            ],
            options={
                'verbose_name': 'Остановка маршрута',
                'verbose_name_plural': 'Остановки маршрутов',
                'ordering': ['order'],
                'unique_together': {('route', 'order')},
            },
        ),
        migrations.AddField(
            model_name='route',
            name='bus_stops',
            field=models.ManyToManyField(through='bus.RouteBusStop', to='bus.busstop', verbose_name='Остановки'),
        ),
        migrations.CreateModel(
            name='Shedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField(verbose_name='Время')),
                ('bus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.bus', verbose_name='Автобус')),
                ('bus_stop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bus.busstop', verbose_name='Остановка')),
            ],
            options={
                'verbose_name': 'Расписание',
                'verbose_name_plural': 'Расписания',
                'unique_together': {('bus', 'bus_stop', 'time')},
            },
        ),
    ]