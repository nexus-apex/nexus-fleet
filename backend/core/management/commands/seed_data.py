from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import Vehicle, Driver, Trip
from datetime import date, timedelta
import random


class Command(BaseCommand):
    help = 'Seed NexusFleet with demo data'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@nexusfleet.com', 'Admin@2024')
            self.stdout.write(self.style.SUCCESS('Admin user created'))

        if Vehicle.objects.count() == 0:
            for i in range(10):
                Vehicle.objects.create(
                    registration=f"Sample {i+1}",
                    vehicle_type=random.choice(["car", "van", "truck", "bus", "bike"]),
                    make=f"Sample {i+1}",
                    model=f"Sample {i+1}",
                    year=random.randint(1, 100),
                    status=random.choice(["active", "maintenance", "retired"]),
                    mileage=random.randint(1, 100),
                    fuel_type=random.choice(["petrol", "diesel", "electric", "cng"]),
                )
            self.stdout.write(self.style.SUCCESS('10 Vehicle records created'))

        if Driver.objects.count() == 0:
            for i in range(10):
                Driver.objects.create(
                    name=["Rajesh Kumar","Priya Sharma","Amit Patel","Deepa Nair","Vikram Singh","Ananya Reddy","Suresh Iyer","Meera Joshi","Karthik Rao","Fatima Khan"][i],
                    license_number=f"Sample {i+1}",
                    phone=f"+91-98765{43210+i}",
                    email=f"demo{i+1}@example.com",
                    status=random.choice(["active", "on_trip", "off_duty", "suspended"]),
                    trips_completed=random.randint(1, 100),
                    rating=round(random.uniform(1000, 50000), 2),
                )
            self.stdout.write(self.style.SUCCESS('10 Driver records created'))

        if Trip.objects.count() == 0:
            for i in range(10):
                Trip.objects.create(
                    vehicle_reg=f"Sample {i+1}",
                    driver_name=f"Sample Trip {i+1}",
                    origin=f"Sample {i+1}",
                    destination=f"Sample {i+1}",
                    distance_km=round(random.uniform(1000, 50000), 2),
                    fuel_cost=round(random.uniform(1000, 50000), 2),
                    start_date=date.today() - timedelta(days=random.randint(0, 90)),
                    status=random.choice(["planned", "in_progress", "completed", "cancelled"]),
                )
            self.stdout.write(self.style.SUCCESS('10 Trip records created'))
