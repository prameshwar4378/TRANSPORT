from django import forms
from Developer.models import *



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

    def clean_vehicle_number(self):
        vehicle_number = self.cleaned_data.get('vehicle_number')
        # Exclude the current instance from uniqueness check
        if Vehicle.objects.filter(vehicle_number=vehicle_number).exclude(id=self.instance.id).exists():
            raise forms.ValidationError("A vehicle with this number already exists.")
        return vehicle_number

    # def clean_owner_mobile_number(self):
    #     mobile_number = self.cleaned_data.get('owner_mobile_number')
    #     if mobile_number:
    #         if not mobile_number.isdigit() or len(mobile_number) != 10:
    #             raise forms.ValidationError("Enter a valid 10-digit mobile number.")
    #     return mobile_number

    # def clean_owner_alternate_mobile_number(self):
    #     alternate_number = self.cleaned_data.get('owner_alternate_mobile_number')
    #     if alternate_number:
    #         if not alternate_number.isdigit() or len(alternate_number) != 10:
    #             raise forms.ValidationError("Enter a valid 10-digit alternate mobile number.")
    #     return alternate_number


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