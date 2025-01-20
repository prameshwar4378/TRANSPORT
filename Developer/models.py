from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Business(models.Model):
    business_name = models.CharField(max_length=100)
    business_label = models.CharField(max_length=15)
    mobile_number = models.CharField(max_length=15)
    alternate_mobile_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    business_number=models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name


class VehicleOwner(models.Model):  
    business = models.ForeignKey(Business, on_delete=models.CASCADE,null=True, blank=True) 
    owner_name = models.CharField(max_length=255)
    owner_mobile_number = models.CharField(max_length=15)
    owner_alternate_mobile_number = models.CharField(max_length=15, null=True, blank=True) 
    pan_card = models.FileField(upload_to='vehicle_owner_documents/pan_cards/', null=True, blank=True)
    adhar_card = models.FileField(upload_to='vehicle_owner_documents/adhar_cards/', null=True, blank=True)
    document1 = models.FileField(upload_to='vehicle_owner_documents/other_documents/', null=True, blank=True)
    document2 = models.FileField(upload_to='vehicle_owner_documents/other_documents/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.owner_name} - {self.owner_mobile_number}"
    


class Vehicle(models.Model): 
    owner = models.ForeignKey(VehicleOwner, on_delete=models.CASCADE, null=True, blank=True) 
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True) 
    vehicle_number = models.CharField(max_length=20, unique=True)  # License plate number
    vehicle_name = models.CharField(max_length=100, null=True, blank=True)
    model_name = models.CharField(max_length=255, null=True, blank=True) 
    notes = models.TextField(null=True, blank=True)
    document1 = models.FileField(upload_to='vehicle_documents/', null=True, blank=True)
    document2 = models.FileField(upload_to='vehicle_documents/', null=True, blank=True) 

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle_name} ({self.vehicle_number})"
    

class Party(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=255)  # Party name
    gst_no = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name="GST Number")
    pan_card = models.FileField(upload_to='party_documents/pan_cards/', null=True, blank=True)
    adhar_card = models.FileField(upload_to='party_documents/adhar_cards/', null=True, blank=True)
    document1 = models.FileField(upload_to='party_documents/other_documents/', null=True, blank=True)
    document2 = models.FileField(upload_to='party_documents/other_documents/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Driver(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True) 
    driver_name = models.CharField(max_length=255)
    licence = models.FileField(upload_to='driver_documents/licence/', null=True, blank=True)
    adhar_card = models.FileField(upload_to='driver_documents/adhar_cards/', null=True, blank=True)
    document1 = models.FileField(upload_to='party_documents/other_documents/', null=True, blank=True)
    document2 = models.FileField(upload_to='party_documents/other_documents/', null=True, blank=True)
    profile_photo = models.ImageField(upload_to='driver_documents/profile_photos/', null=True, blank=True)

    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    alternate_mobile = models.CharField(max_length=15, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 
    def __str__(self):
        return self.driver_name
    


class CustomUser(AbstractUser):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True) 
    is_business=models.BooleanField(default=True)



