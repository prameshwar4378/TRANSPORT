from django import forms
from Developer.models import *
from django.core.exceptions import ValidationError


class OwnerForm(forms.ModelForm):
    class Meta:
        model = VehicleOwner
        fields = [
            'owner_name',
            'owner_mobile_number',
            'owner_alternate_mobile_number',
            'pan_card',
            'adhar_card',
            'document1',
            'document2',
        ] 

    def clean(self):
        cleaned_data = super().clean()
        owner_name = cleaned_data.get('owner_name')
        owner_mobile_number = cleaned_data.get('owner_mobile_number')

        # Only perform the validation if it's a new record (i.e., during creation)
        if self.instance.pk is None:  # If the instance doesn't have a primary key, it's new
            if VehicleOwner.objects.filter(owner_name__iexact=owner_name, owner_mobile_number=owner_mobile_number).exists():
                raise ValidationError(
                    f"An owner with the name '{owner_name}' and mobile number '{owner_mobile_number}' already exists."
                )

        return cleaned_data




class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [  
            'vehicle_name',
            'vehicle_number',
            'model_name', 
            'notes',
            'document1',
            'document2', 
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        } 



class VehicleUpdateForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [  
            'owner',
            'vehicle_name',
            'vehicle_number',
            'model_name', 
            'notes',
            'document1',
            'document2', 
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        } 


        

class PartyForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = [
            'name',
            'gst_no',
            'pan_card',
            'adhar_card',
            'document1',
            'document2',
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter party name'}),
            'gst_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter GST Number'}),
        }

    def clean_gst_no(self):
        gst_no = self.cleaned_data.get('gst_no')
        if gst_no and len(gst_no) != 15:
            raise forms.ValidationError("GST Number must be exactly 15 characters long.")
        return gst_no

    def clean_pan_card(self):
        pan_card = self.cleaned_data.get('pan_card')
        if pan_card and not str(pan_card).lower().endswith(('.pdf', '.jpg', '.png')):
            raise forms.ValidationError("PAN Card must be a PDF, JPG, or PNG file.")
        return pan_card

    def clean_adhar_card(self):
        adhar_card = self.cleaned_data.get('adhar_card')
        if adhar_card and not str(adhar_card).lower().endswith(('.pdf', '.jpg', '.png')):
            raise forms.ValidationError("Aadhar Card must be a PDF, JPG, or PNG file.")
        return adhar_card




class DriverForm(forms.ModelForm):
    class Meta:
        model = Driver
        fields = [
            'driver_name',
            'licence',
            'adhar_card',
            'document1',
            'document2',
            'profile_photo',
            'mobile',
            'alternate_mobile',
        ]
        widgets = {
            'driver_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter driver name'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter mobile number'}),
            'alternate_mobile': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter alternate mobile number'}),
        }

    def clean_mobile(self):
        mobile = self.cleaned_data.get('mobile')
        if mobile and (not mobile.isdigit() or len(mobile) != 10):
            raise forms.ValidationError("Enter a valid 10-digit mobile number.")
        return mobile

    def clean_alternate_mobile(self):
        alternate_mobile = self.cleaned_data.get('alternate_mobile')
        if alternate_mobile and (not alternate_mobile.isdigit() or len(alternate_mobile) != 10):
            raise forms.ValidationError("Enter a valid 10-digit alternate mobile number.")
        return alternate_mobile

    def clean_licence(self):
        licence = self.cleaned_data.get('licence')
        if licence and not str(licence).lower().endswith(('.pdf', '.jpg', '.png')):
            raise forms.ValidationError("Licence must be a PDF, JPG, or PNG file.")
        return licence

    def clean_adhar_card(self):
        adhar_card = self.cleaned_data.get('adhar_card')
        if adhar_card and not str(adhar_card).lower().endswith(('.pdf', '.jpg', '.png')):
            raise forms.ValidationError("Aadhar Card must be a PDF, JPG, or PNG file.")
        return adhar_card
    



 

# class BillForm(forms.Form):
#     from_location = forms.CharField(
#         max_length=255, 
#         label="From Location", 
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
 
#     to_location = forms.CharField(
#         max_length=255, 
#         label="To Location", 
#         widget=forms.TextInput(attrs={'class': 'form-control'})
#     )
#     material_type = forms.CharField(
#         max_length=255, 
#         label="Type of Material", 
#         widget=forms.TextInput(attrs={'class': 'form-control'}),
#         required=False, 
#     )
#     rent_amount = forms.DecimalField(
#         max_digits=10, 
#         decimal_places=2, 
#         label="Rent Amount", 
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'oninput': 'calculate_pending_amount()'})
#     )
#     advance_amount = forms.DecimalField(
#         max_digits=10, 
#         decimal_places=2, 
#         label="Advance Amount", 
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'oninput': 'calculate_pending_amount()'})
#     )
#     pending_amount = forms.DecimalField(
#         max_digits=10, 
#         decimal_places=2, 
#         label="Pending Amount", 
#         widget=forms.NumberInput(attrs={'class': 'form-control', 'readonly': True})
#     )
#     commission = forms.DecimalField(
#         max_digits=10, 
#         decimal_places=2, 
#         label="Commission", 
#         required=False, 
#         widget=forms.NumberInput(attrs={'class': 'form-control'})
#     )
#     notes = forms.CharField(
#         label="Additional Notes", 
#         required=False, 
#         widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
#     )


#     # Add the missing fields
#     driver = forms.CharField(
#         max_length=255,
#         label="Driver",
#         widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'driverdata'})
#     )
#     vehicle = forms.CharField(
#         max_length=255,
#         label="Vehicle",
#         widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'vehicledata'})
#     )
#     owner = forms.CharField(
#         max_length=255,
#         label="Owner",
#         widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'ownerdata'})
#     )
#     party = forms.CharField(
#         max_length=255,
#         label="Party",
#         widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'partydata'})
#     )
    
#     # Custom Validation
#     def clean(self):
#         cleaned_data = super().clean()
#         rent_amount = cleaned_data.get('rent_amount')
#         advance_amount = cleaned_data.get('advance_amount')

#         if advance_amount is not None and rent_amount is not None:
#             if advance_amount > rent_amount:
#                 raise forms.ValidationError("Advance amount cannot be greater than rent amount.")
 
#         driver = cleaned_data.get('driver')
#         vehicle = cleaned_data.get('vehicle')
#         party = cleaned_data.get('party')
#         owner = cleaned_data.get('owner')

#         print(driver) 
#         print(vehicle)
#         print(party)
#         print(owner)
        
#         return cleaned_data

# def save(self, commit=True):
#     # Save the data to the database or process it as needed
#     data = self.cleaned_data
#     vehicle = data.get('vehicle')
    
#     # Retrieve the vehicle instance using the vehicle_number
#     vehicle = Vehicle.objects.filter(vehicle_number=vehicle).first()

#     # Create the Bill object and save it
#     bill = Bill.objects.create(
#         from_location=data['from_location'],
#         to_location=data['to_location'],
#         material_type=data['material_type'],
#         rent_amount=data['rent_amount'],
#         advance_amount=data['advance_amount'],
#         pending_amount=data['pending_amount'],
#         commission=data['commission'],
#         notes=data['notes'],
#         business=self.request.user.business,  # Assuming 'business' is related to the user
#         vehicle=vehicle,
#     ).save()
#     return bill



class BillForm(forms.ModelForm):

    # Add the missing fields
    driver = forms.CharField(
        max_length=255,
        label="Driver",
        widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'driverdata'})
    )
    vehicle = forms.CharField(
        max_length=255,
        label="Vehicle",
        widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'vehicledata'})
    )
    owner = forms.CharField(
        max_length=255,
        label="Owner",
        widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'ownerdata'})
    )
    party = forms.CharField(
        max_length=255,
        label="Party",
        widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'partydata'})
    )
    
    class Meta:
        model = Bill
        fields = [
            'from_location', 'to_location', 'material_type', 'rent_amount', 'advance_amount',
            'pending_amount', 'commission', 'notes'
        ]

        widgets = {
            'rent_amount': forms.TextInput(attrs={'oninput': 'calculate_pending_amount()'}),
            'advance_amount': forms.TextInput(attrs={'oninput': 'calculate_pending_amount()'}),
        }
    # Custom Validation
    def clean(self):
        cleaned_data = super().clean()
        rent_amount = cleaned_data.get('rent_amount')
        advance_amount = cleaned_data.get('advance_amount')

        if advance_amount is not None and rent_amount is not None:
            if advance_amount > rent_amount:
                raise forms.ValidationError("Advance amount cannot be greater than rent amount.")
 
        driver = cleaned_data.get('driver')
        vehicle = cleaned_data.get('vehicle')
        party = cleaned_data.get('party')
        owner = cleaned_data.get('owner')

        print(driver) 
        print(vehicle)
        print(party)
        print(owner)
        
        return cleaned_data
     