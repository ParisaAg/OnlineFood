from django import forms
from .models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=20,widget=forms.PasswordInput())
    password_confirmation=forms.CharField(max_length=20,widget=forms.PasswordInput())
    class Meta :
        model = User
        fields =  [ 'first_name', 'last_name', 'username', 'email', 'phone_number','password','password_confirmation']
    def clean(self):
        cleaned_data= super(UserForm,self).clean()
        password=cleaned_data.get('password')
        password_confirmation=cleaned_data.get('password_confirmation')
        if password_confirmation != password:
            raise forms.ValidationError(
                "password does not match"
            )