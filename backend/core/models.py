from django.db import models

class Vehicle(models.Model):
    registration = models.CharField(max_length=255)
    vehicle_type = models.CharField(max_length=50, choices=[("car", "Car"), ("van", "Van"), ("truck", "Truck"), ("bus", "Bus"), ("bike", "Bike")], default="car")
    make = models.CharField(max_length=255, blank=True, default="")
    model = models.CharField(max_length=255, blank=True, default="")
    year = models.IntegerField(default=0)
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("maintenance", "Maintenance"), ("retired", "Retired")], default="active")
    mileage = models.IntegerField(default=0)
    fuel_type = models.CharField(max_length=50, choices=[("petrol", "Petrol"), ("diesel", "Diesel"), ("electric", "Electric"), ("cng", "CNG")], default="petrol")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.registration

class Driver(models.Model):
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=255, blank=True, default="")
    phone = models.CharField(max_length=255, blank=True, default="")
    email = models.EmailField(blank=True, default="")
    status = models.CharField(max_length=50, choices=[("active", "Active"), ("on_trip", "On Trip"), ("off_duty", "Off Duty"), ("suspended", "Suspended")], default="active")
    trips_completed = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Trip(models.Model):
    vehicle_reg = models.CharField(max_length=255)
    driver_name = models.CharField(max_length=255, blank=True, default="")
    origin = models.CharField(max_length=255, blank=True, default="")
    destination = models.CharField(max_length=255, blank=True, default="")
    distance_km = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    fuel_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    start_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[("planned", "Planned"), ("in_progress", "In Progress"), ("completed", "Completed"), ("cancelled", "Cancelled")], default="planned")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.vehicle_reg
