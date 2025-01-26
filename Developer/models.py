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
        if self.vehicle_name:
            return f"{self.vehicle_name} - ({self.vehicle_number[:-5]} {self.vehicle_number[-4:]})"
        else:
            return f"{self.vehicle_number[:-5]} {self.vehicle_number[-4:]}"
    
 
class Party(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=255)  # Party name
    gst_no = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name="GST Number")
    pan_card = models.FileField(upload_to='party_documents/pan_cards/', null=True, blank=True)
    adhar_card = models.FileField(upload_to='party_documents/adhar_cards/', null=True, blank=True)
    document1 = models.FileField(upload_to='party_documents/other_documents/', null=True, blank=True)
    document2 = models.FileField(upload_to='party_documents/other_documents/', null=True, blank=True)

    mobile = models.CharField(max_length=15, unique=True, null=True, blank=True)
    alternate_mobile = models.CharField(max_length=15, null=True, blank=True)

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



from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError

class Bill(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True, blank=True) 
    bill_number = models.CharField(max_length=10, unique=True, editable=False)
    party = models.ForeignKey(
        'Party', on_delete=models.SET_NULL, related_name='bills', verbose_name="Party Name", null=True, blank=True
    ) 
    driver = models.ForeignKey(
        'Driver', on_delete=models.SET_NULL, null=True, blank=True, related_name='bills', verbose_name="Driver"
    )
    vehicle = models.ForeignKey(
        'Vehicle', on_delete=models.CASCADE,  related_name='bills', verbose_name="Vehicle"
    )

    referece = models.ForeignKey(
        'VehicleOwner', on_delete=models.SET_NULL, null=True, blank=True, related_name='referenced_bills', verbose_name="Referenced Owner"
    )
    
    date_time = models.DateTimeField(default=now, verbose_name="Bill Date & Time")
    from_location = models.CharField(max_length=255, verbose_name="From Location")
    to_location = models.CharField(max_length=255, verbose_name="To Location")
    material_type = models.CharField(max_length=255, null=True, blank=True, verbose_name="Type of Material")
    rent_amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Rent Amount")
    advance_amount = models.DecimalField(max_digits=10, decimal_places=0, verbose_name="Advance Amount")
    pending_amount = models.DecimalField(max_digits=10, decimal_places=0, default=0, verbose_name="Pending Amount")
    commission = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True,default=0,  verbose_name="Commission")
    
    notes = models.TextField(null=True, blank=True, verbose_name="Additional Notes")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        verbose_name = "Bill"
        verbose_name_plural = "Bills"
        ordering = ['-created_at']

    def __str__(self):
        return f"Bill #{self.bill_number} for {self.party.name}"

    def clean(self):
        """
        Ensure that the pending amount is always calculated correctly.
        """
        if self.pending_amount != (self.rent_amount - self.advance_amount):
            raise ValidationError(
                "Pending amount must be equal to Rent Amount minus Advance Amount."
            )

    def save(self, *args, **kwargs):
        """
        Generate the bill number automatically if it’s a new record.
        """
        if not self.bill_number:
            last_bill = Bill.objects.order_by('id').last()
            if last_bill:
                bill_number = int(last_bill.bill_number) + 1
            else:
                bill_number = 1
            self.bill_number = str(bill_number).zfill(5)  # Auto-generate e.g., 00001, 00002
        super().save(*args, **kwargs)