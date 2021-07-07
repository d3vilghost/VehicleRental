from django.contrib import admin
from .models import UserProfile, VehicleType, Vehicle, RentVehicle
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Vehicle)
admin.site.register(VehicleType)
admin.site.register(RentVehicle)