
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError



class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
 



class CustomUserForm(UserCreationForm): 
    class Meta:
        model = CustomUser
        fields = ("username",'first_name','last_name','business', "password1", "password2", 'is_active')
 
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if CustomUser.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("A user with that username already exists.")
        return username


class UpdatePasswordForm(forms.Form):
    new_password1 = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}),
        min_length=8
    )
    new_password2 = forms.CharField(
        label="Confirm New Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm new password'}),
        min_length=8
    )

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("new_password1")
        password2 = cleaned_data.get("new_password2")

        # Check if the passwords match
        if password1 != password2:
            raise ValidationError("The two password fields must match.")
        return cleaned_data
 


class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = [
            'business_name',
            'business_label',
            'mobile_number',
            'alternate_mobile_number',
            'address',
            'email',
        ]

        # Optional: Add widgets to customize form field rendering
        widgets = {
            'business_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Business Name'}),
            'business_label': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Business Label'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Mobile Number'}),
            'alternate_mobile_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Alternate Mobile Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Address', 'rows': 3}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter Email Address'}),
        }

        # Optional: Add labels for better readability
        labels = {
            'business_name': 'Business Name',
            'business_label': 'Business Label',
            'mobile_number': 'Mobile Number',
            'alternate_mobile_number': 'Alternate Mobile Number',
            'address': 'Address',
            'email': 'Email Address',
        }

        # Optional: Add help texts to guide the user
        help_texts = {
            'email': 'Ensure the email is valid and unique.',
        }