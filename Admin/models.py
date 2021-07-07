import random

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    USER_TYPES = [
        ('Owner', 'Owner'),
        ('Admin', 'Admin'),
        ('Public', 'Public'),
    ]
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    profilePicture = models.ImageField(blank=True, null=True)
    contact_No = models.IntegerField()
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    userType = models.CharField(max_length=15, choices=USER_TYPES, default='Public')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.user.username


class OTP(models.Model):
    def Get_OTP():
        return random.randint(100000, 999999)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField(default=Get_OTP)
    created_at = models.DateTimeField(auto_now_add=True)


class VehicleType(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Vehicle(models.Model):
    STATUS = (
        ('Not Available', 'Not Available'),
        ('Available','Available')
    )
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vehicle_type = models.ForeignKey(VehicleType, on_delete=models.CASCADE)
    vehiclenumber = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    image = models.ImageField()
    price_per_day = models.IntegerField()
    status = models.CharField(max_length=15, choices=STATUS, default='Available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class RentVehicle(models.Model):
    STATUS = (
        ('Pending','Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
        ('On Rent', 'On Rent'),
        ('Completed Rent','Completed Rent')
    )

    PAID_STATUS = (
        ('UnPaid', 'UnPaid'),
        ('Paid', 'Paid')
    )

    def BookingId():
        return int(random.randint(10000000,99999999))
    
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    booking_id = models.IntegerField(default=BookingId)
    aadhar_number = models.BigIntegerField()
    id_proof = models.ImageField()
    book_day = models.SmallIntegerField()
    book_from = models.DateField()
    book_to = models.DateField()
    total_price = models.IntegerField(null=True)
    paid_status = models.CharField(max_length=15, choices=PAID_STATUS, default="UnPaid")
    status = models.CharField(max_length=15, choices=STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.booking_id} by {self.user.user.id}'
