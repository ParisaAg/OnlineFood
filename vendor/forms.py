from django import forms
from .models import Vendor
from accounts.validators import allow_only_img


class VendorForm(forms.ModelForm):
    license=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_img])
    class Meta:
        model= Vendor
        fields = ['vendor_name', 'license']


