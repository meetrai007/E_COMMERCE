from django import forms
from .models import Userprofile
from orders.models import ProductReview

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
# forms.py
from django import forms

class AddressForm(forms.Form):
    delivery_address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter your delivery address'}), required=True)



