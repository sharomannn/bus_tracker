from django.contrib import admin
from .models import *


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('number', 'car_number', 'image_tag')
    readonly_fields = ('image_tag',)


@admin.register(CarNumber)
class CarNumberAdmin(admin.ModelAdmin):
    list_display = ('number',)


@admin.register(BusProxy)
class BusProxyAdmin(admin.ModelAdmin):
    list_display = ('number', 'car_number')


@admin.register(BusStop)
class BusStopAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude')


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(BusDriver)
class BusDriverAdmin(admin.ModelAdmin):
    list_display = ('bus', 'driver', 'date')


@admin.register(RouteBusStop)
class RouteBusStopAdmin(admin.ModelAdmin):
    list_display = ('route', 'bus_stop', 'order')