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

    owner = forms.CharField(
        max_length=255,
        label="",
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'ownerdata'})
    )
    
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

    # Custom validation for owner field
    def clean_owner(self):
        name_pattern = r"^[A-Za-z ]+$"  # Matches names with alphabets and spaces
        phone_pattern = r"^\d{10}$"  # Matches a 10-digit mobile number

        owner = self.cleaned_data.get('owner')  # Data format can be: "Suresh Jadhav - 8888888888", "Suresh Jadhav", "8888888888", etc.
        owner = str(owner).strip()

        if owner:
            if '-' in owner:
                # Split the input into name and mobile number
                parts = owner.split(' - ', 1)
                if len(parts) != 2:
                    raise forms.ValidationError("Invalid owner data format. Should be 'Name - Mobile Number'.")
                name, mobile_number = parts
                name = name.strip()
                mobile_number = mobile_number.strip()
                # Validate name and mobile number separately
                if not re.match(name_pattern, name):
                    raise forms.ValidationError("Invalid owner name format.")
                if not re.match(phone_pattern, mobile_number):
                    raise forms.ValidationError("Invalid owner mobile number format. Ensure it's exactly 10 digits.")
            else:
                # Case when owner is just a name or just a mobile number
                # if not (re.match(name_pattern, owner) or re.match(phone_pattern, owner)):
                #     raise forms.ValidationError("Invalid owner data format. Please provide either a valid name or a valid mobile number.")
                raise forms.ValidationError("Invalid owner data format. Should be 'Name - Mobile Number'.")
        return owner
    

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
            'mobile',
            'alternate_mobile',
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
    

 
import re


class BillForm(forms.ModelForm):

    # Add the missing fields
    driver = forms.CharField(
        max_length=255,
        label="Driver",
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'driverdata'})
    )
    vehicle = forms.CharField(
        max_length=255,
        label="Vehicle",
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'vehicledata'}),
        error_messages={
        'required': 'Vehicle Number are required.',
    }
    )
    owner = forms.CharField(
        max_length=255,
        label="Owner",
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'ownerdata'})
    )
    party = forms.CharField(
        max_length=255,
        label="Party",
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'partydata'})
    )
    
    reference = forms.CharField(
        max_length=255,
        label="Reference",
        required=False, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'list': 'ownerdata'})
    )
    
    class Meta:
        model = Bill
        fields = [
            'from_location', 'to_location', 'material_type', 'rent_amount', 'advance_amount',
            'pending_amount', 'commission_charge', 'commission_received', 'commission_pending', 'notes'
        ]
        widgets = {
            'vehicle': forms.TextInput(attrs={'onkeyup': 'get_owner_details()'}),
            'rent_amount': forms.TextInput(attrs={'oninput': 'calculate_pending_amount()'}),
            'advance_amount': forms.TextInput(attrs={'oninput': 'calculate_pending_amount()'}),
            'commission_charge': forms.TextInput(attrs={'oninput': 'calculate_commission_pending()'}),
            'commission_received': forms.TextInput(attrs={'oninput': 'calculate_commission_pending()'}),
            'notes': forms.TextInput(attrs={'row': 3}),
        }
 
    def clean(self):
        cleaned_data = super().clean()
        rent_amount = cleaned_data.get('rent_amount')
        advance_amount = cleaned_data.get('advance_amount')
        if advance_amount is not None and rent_amount is not None:
            if advance_amount > rent_amount:
                raise forms.ValidationError("Advance amount cannot be greater than rent amount.")
        return cleaned_data

    def clean_vehicle(self):
        vehicle = self.cleaned_data.get('vehicle')
        if ' ' in vehicle:
            raise ValidationError("Spaces are not allowed in the Vehicle field.")
        return vehicle
    
    # Custom validation for driver field
    def clean_driver(self):
        name_pattern = r"^[A-Za-z ]+$"  # Matches names with alphabets and spaces
        phone_pattern = r"^\d{10}$"  # Matches a 10-digit mobile number

        driver = self.cleaned_data.get('driver')  # Data format can be: "Suresh Jadhav - 8888888888", "Suresh Jadhav", "8888888888", etc.
        driver = str(driver).strip()

        if driver:
            if '-' in driver:
                # Split the input into name and mobile number
                parts = driver.split(' - ', 1)
                
                if len(parts) != 2:
                    raise forms.ValidationError("Invalid driver data format. Should be 'Name - Mobile Number'.")
                
                name, mobile_number = parts
                name = name.strip()
                mobile_number = mobile_number.strip()

                # Validate name and mobile number separately
                if not re.match(name_pattern, name):
                    raise forms.ValidationError("Invalid driver name format.")
                if not re.match(phone_pattern, mobile_number):
                    raise forms.ValidationError("Invalid driver mobile number format. Ensure it's exactly 10 digits.")
            else:
                raise forms.ValidationError("Invalid driver data format. Should be 'Name - Mobile Number'.")
        return driver
    
    # Custom validation for owner field
    def clean_owner(self):
        name_pattern = r"^[A-Za-z ]+$"  # Matches names with alphabets and spaces
        phone_pattern = r"^\d{10}$"  # Matches a 10-digit mobile number

        owner = self.cleaned_data.get('owner')  # Data format can be: "Suresh Jadhav - 8888888888", "Suresh Jadhav", "8888888888", etc.
        owner = str(owner).strip()

        if owner:
            if '-' in owner:
                # Split the input into name and mobile number
                parts = owner.split(' - ', 1)
                
                if len(parts) != 2:
                    raise forms.ValidationError("Invalid owner data format. Should be 'Name - Mobile Number'.")
                
                name, mobile_number = parts
                name = name.strip()
                mobile_number = mobile_number.strip()
                if not name:
                    raise forms.ValidationError("Invalid owner data format. Should be 'Name - Mobile Number")                
                # Validate name and mobile number separately
                if not re.match(name_pattern, name):
                    raise forms.ValidationError("Invalid owner name format.")
                if not re.match(phone_pattern, mobile_number):
                    raise forms.ValidationError("Invalid owner mobile number format. Ensure it's exactly 10 digits.")
            else:
                raise forms.ValidationError("Invalid owner data format. Should be 'Name - Mobile Number'.")
        
        return owner
    


    # Custom validation for reference field
    def clean_reference(self):
        name_pattern = r"^[A-Za-z ]+$"  # Matches names with alphabets and spaces
        phone_pattern = r"^\d{10}$"  # Matches a 10-digit mobile number

        reference = self.cleaned_data.get('reference')  # Data format can be: "Suresh Jadhav - 8888888888", "Suresh Jadhav", "8888888888", etc.
        reference = str(reference).strip()

        if reference:
            if '-' in reference:
                # Split the input into name and mobile number
                parts = reference.split(' - ', 1)
                
                if len(parts) != 2:
                    raise forms.ValidationError("Invalid reference data format. Should be 'Name - Mobile Number'.")
                
                name, mobile_number = parts
                name = name.strip()
                mobile_number = mobile_number.strip()
                if not name:
                    raise forms.ValidationError("Invalid reference data format. Should be 'Name - Mobile Number")                
                # Validate name and mobile number separately
                if not re.match(name_pattern, name):
                    raise forms.ValidationError("Invalid reference name format.")
                if not re.match(phone_pattern, mobile_number):
                    raise forms.ValidationError("Invalid reference mobile number format. Ensure it's exactly 10 digits.")
            else:
                raise forms.ValidationError("Invalid reference data format. Should be 'Name - Mobile Number'.")
        
        return reference
    
    
    # Custom validation for party field
    def clean_party(self):
        name_pattern = r"^[A-Za-z ]+$"  # Matches names with alphabets and spaces
        phone_pattern = r"^\d{10}$"  # Matches a 10-digit mobile number

        party = self.cleaned_data.get('party')  # Data format can be: "Suresh Jadhav - 8888888888", "Suresh Jadhav", "8888888888", etc.
        party = str(party).strip()

        if party:
            if '-' in party:
                # Split the input into name and mobile number
                parts = party.split(' - ', 1)
                
                if len(parts) != 2:
                    raise forms.ValidationError("Invalid party data format. Should be 'Name - Mobile Number'.")
                
                name, mobile_number = parts
                name = name.strip()
                mobile_number = mobile_number.strip()
                if not name:
                    raise forms.ValidationError("Invalid party data format. Should be 'Name - Mobile Number")
                                
                # Validate name and mobile number separately
                if not re.match(name_pattern, name):
                    raise forms.ValidationError("Invalid party name format.")
                if not re.match(phone_pattern, mobile_number):
                    raise forms.ValidationError("Invalid party mobile number format. Ensure it's exactly 10 digits.")
            else:
                # Case when party is just a name or just a mobile number
                # if not (re.match(name_pattern, party) or re.match(phone_pattern, party)):
                #     raise forms.ValidationError("Invalid party data format. Please provide either a valid name or a valid mobile number.")
                raise forms.ValidationError("Invalid party data format. Should be 'Name - Mobile Number'.")
        
        return party
    
    
class BillUpdateForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = [
            'vehicle','driver','party','from_location', 'to_location', 'material_type', 'rent_amount', 'advance_amount',
            'pending_amount', 'commission_charge', 'commission_received', 'commission_pending', 'notes', 'reference'
        ]

        widgets = {
            'rent_amount': forms.TextInput(attrs={'oninput': 'calculate_pending_amount()'}),
            'advance_amount': forms.TextInput(attrs={'oninput': 'calculate_pending_amount()'}),
            'commission_charge': forms.TextInput(attrs={'oninput': 'calculate_commission_pending()'}),
            'commission_received': forms.TextInput(attrs={'oninput': 'calculate_commission_pending()'}),
            'notes': forms.TextInput(attrs={'row': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        rent_amount = cleaned_data.get('rent_amount')
        advance_amount = cleaned_data.get('advance_amount')
        if advance_amount is not None and rent_amount is not None:
            if advance_amount > rent_amount:
                raise forms.ValidationError("Advance amount cannot be greater than rent amount.")
        return cleaned_data
     
