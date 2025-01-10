from django import forms
from .models import Userprofile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Userprofile
        fields = ['phone_number', 'profile_picture', 'first_name', 'last_name']
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
