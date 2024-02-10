from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.html import format_html
from django.core.exceptions import ValidationError


class Vehicle(models.Model):
    number = models.CharField(max_length=10, unique=True)

    class Meta:
        abstract = True


class CarNumber(Vehicle):
    class Meta:
        verbose_name = 'Номер машины'
        verbose_name_plural = 'Номера машин'

    def __str__(self):
        return self.number


class Bus(Vehicle):
    car_number = models.ForeignKey(CarNumber, on_delete=models.CASCADE, verbose_name='Номер машины')
    image = models.ImageField(upload_to='bus_images/', verbose_name='Изображение автобуса', null=True, blank=True)
    driver = models.ManyToManyField('Driver', through='BusDriver', verbose_name='Водители')

    def image_tag(self):
        if self.image:
            return format_html('<img src="{}" width="150" height="150" />', self.image.url)
        else:
            return 'No Image'

    image_tag.short_description = 'Image'

    class Meta:
        verbose_name = 'Автобус'
        verbose_name_plural = 'Автобусы'

    def __str__(self):
        return self.number


class BusProxy(Bus):
    class Meta:
        proxy = True


class Driver(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя водителя')

    class Meta:
        verbose_name = 'Водитель'
        verbose_name_plural = 'Водители'

    def __str__(self):
        return self.name


class BusDriver(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name='Автобус')
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, verbose_name='Водитель')
    date = models.DateField(verbose_name='Дата')

    class Meta:
        verbose_name = 'Водитель автобуса'
        verbose_name_plural = 'Водители автобусов'

    def __str__(self):
        return f'{self.bus} - {self.driver} - {self.date}'


class BusStop(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название остановки')
    latitude = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)], verbose_name='Широта',
                                 blank=True)
    longitude = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)], verbose_name='Долгота',
                                  blank=True)
    nearby_stops = models.ManyToManyField('self', blank=True)

    class Meta:
        verbose_name = 'Остановка'
        verbose_name_plural = 'Остановки'

    def __str__(self):
        return self.name


class Shedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, verbose_name='Автобус')
    bus_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, verbose_name='Остановка')
    time = models.TimeField(verbose_name='Время')

    class Meta:
        verbose_name = 'Расписание'
        verbose_name_plural = 'Расписания'
        unique_together = ('bus', 'bus_stop', 'time')

    def __str__(self):
        return f'{self.bus} - {self.bus_stop} - {self.time}'


class Route(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название маршрута')
    bus_stops = models.ManyToManyField(BusStop, through='RouteBusStop', verbose_name='Остановки')

    class Meta:
        verbose_name = 'Маршрут'
        verbose_name_plural = 'Маршруты'

    def __str__(self):
        return self.name


class RouteBusStop(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, verbose_name='Маршрут')
    bus_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, verbose_name='Остановка')
    order = models.PositiveIntegerField(verbose_name='Порядок следования')

    class Meta:
        verbose_name = 'Остановка маршрута'
        verbose_name_plural = 'Остановки маршрутов'
        unique_together = ('route', 'order')
        ordering = ['order']

    def __str__(self):
        return f'{self.route} - {self.bus_stop} - {self.order}'
