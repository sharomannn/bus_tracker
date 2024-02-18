from django.db.models import Q, F
from django.test import TestCase
from bus.models import *


class BusTestCase(TestCase):
    def setUp(self):
        car_number1 = CarNumber.objects.create(number='123ABC')
        car_number2 = CarNumber.objects.create(number='456DEF')

        bus1 = Bus.objects.create(number='Bus1', car_number=car_number1)
        bus2 = Bus.objects.create(number='Bus2', car_number=car_number2)

        driver1 = Driver.objects.create(name='Driver1')
        driver2 = Driver.objects.create(name='Driver2')

        BusDriver.objects.create(bus=bus1, driver=driver1, date='2022-01-01')
        BusDriver.objects.create(bus=bus2, driver=driver2, date='2022-01-02')

        bus_stop1 = BusStop.objects.create(name='Stop1', latitude=50.4501, longitude=30.5234)
        bus_stop2 = BusStop.objects.create(name='Stop2', latitude=50.4502, longitude=30.5235)

        route1 = Route.objects.create(name='Route1')
        route2 = Route.objects.create(name='Route2')

        RouteBusStop.objects.create(route=route1, bus_stop=bus_stop1, order=1)
        RouteBusStop.objects.create(route=route2, bus_stop=bus_stop2, order=2)

        Shedule.objects.create(bus=bus1, bus_stop=bus_stop1, time='10:00')
        Shedule.objects.create(bus=bus2, bus_stop=bus_stop2, time='11:00')

    def test_bus(self):
        all_buses = Bus.objects.all()
        self.assertEqual(all_buses.count(), 2)
        print(all_buses)

        buses_with_number = Bus.objects.filter(number='Bus1')
        self.assertEqual(buses_with_number.count(), 1)
        print(buses_with_number)

        buses_with_number_and_driver = Bus.objects.filter(number='Bus1', driver__name='Driver1')
        self.assertEqual(buses_with_number_and_driver.count(), 1)
        print(buses_with_number_and_driver)

        bus = Bus.objects.get(number='Bus1')
        self.assertEqual(bus.number, 'Bus1')
        print(bus)

        first_bus = Bus.objects.all().first()
        self.assertEqual(first_bus.number, 'Bus1')
        print(first_bus)

        buses_with_number = Bus.objects.filter(number__contains='Bus')
        self.assertEqual(buses_with_number.count(), 2)
        print(buses_with_number)

        buses_with_driver = Bus.objects.filter(driver__name='Driver1')
        self.assertEqual(buses_with_driver.count(), 1)
        print(buses_with_driver)

        driver1 = Driver.objects.get(name='Driver1')
        buses_with_driver = Bus.objects.filter(driver__name=driver1.name)
        self.assertEqual(buses_with_driver.count(), 1)
        print(buses_with_driver)

        car_number = CarNumber.objects.get(number='123ABC')
        buses = car_number.bus_set.all()
        self.assertEqual(buses.count(), 1)
        print(buses)

        driver = Driver.objects.get(name='Driver1')
        buses = driver.bus_set.all()
        self.assertEqual(buses.count(), 1)
        print(buses)

        Bus.objects.get(car_number__number='123ABC').delete()
        self.assertEqual(Bus.objects.filter(number='NewBus').count(), 0)
        print(Bus.objects.filter(number='NewBus'))


class BusTestCase2(BusTestCase):
    def test_filter(self):
        print("Running test_filter")
        buses_with_number = Bus.objects.filter(number='Bus1')
        self.assertEqual(buses_with_number.count(), 1)
        print(buses_with_number)

    def test_exclude(self):
        print("Running test_exclude")
        buses_without_number = Bus.objects.exclude(number='Bus1')
        self.assertEqual(buses_without_number.count(), 1)
        print(buses_without_number)

    def test_annotate(self):
        print("Running test_annotate")
        from django.db.models import Count
        buses_with_driver_count = Bus.objects.annotate(driver_count=Count('driver'))
        for bus in buses_with_driver_count:
            print(f'{bus.number}: {bus.driver_count}')

    def test_order_by(self):
        print("Running test_order_by")
        buses_ordered_by_number = Bus.objects.order_by('number')
        for bus in buses_ordered_by_number:
            print(bus.number)

    def test_reverse(self):
        print("Running test_reverse")
        buses_ordered_by_number = Bus.objects.order_by('number')
        buses_reversed = buses_ordered_by_number.reverse()
        for bus in buses_reversed:
            print(bus.number)

    def test_values(self):
        print("Running test_values")
        bus_values = Bus.objects.values('number', 'car_number')
        for bus_value in bus_values:
            print(bus_value)

    def test_values_list(self):
        print("Running test_values_list")
        bus_values_list = Bus.objects.values_list('number', 'car_number')
        for bus_value_list in bus_values_list:
            print(bus_value_list)

    def test_get_or_create(self):
        print("Running test_get_or_create")
        bus, created = Bus.objects.get_or_create(number='Bus3', car_number=CarNumber.objects.get(number='123ABC'))
        print(f"Get or create test: {bus}, created: {created}")

    def test_update_or_create(self):
        print("Running test_update_or_create")
        bus, created = Bus.objects.update_or_create(number='Bus1', defaults={'number': 'Bus3'})
        print(f"Update or create test: {bus}, created: {created}")


    def test_bulk_update(self):
        print("Running test_bulk_update")
        buses = list(Bus.objects.filter(number__startswith='Bus'))
        for bus in buses:
            bus.number = 'Updated ' + bus.number
        Bus.objects.bulk_update(buses, ['number'])
        for bus in buses:
            print(f"Bulk update test: {bus}")

    def test_q(self):
        print("Running test_q")
        buses = Bus.objects.filter(Q(number__startswith='Bus') & ~Q(car_number__number='123ABC'))
        print(f"Q test: {buses}")

    def test_f(self):
        print("Running test_f")
        BusStop.objects.update(latitude=F('latitude') + 1)
        bus_stops = BusStop.objects.filter(latitude__gt=50.4501)
        print(f"F test: {bus_stops}")
