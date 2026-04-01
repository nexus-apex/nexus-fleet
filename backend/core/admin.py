from django.contrib import admin
from .models import Vehicle, Driver, Trip

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ["registration", "vehicle_type", "make", "model", "year", "created_at"]
    list_filter = ["vehicle_type", "status", "fuel_type"]
    search_fields = ["registration", "make", "model"]

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ["name", "license_number", "phone", "email", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["name", "license_number", "phone"]

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ["vehicle_reg", "driver_name", "origin", "destination", "distance_km", "created_at"]
    list_filter = ["status"]
    search_fields = ["vehicle_reg", "driver_name", "origin"]
