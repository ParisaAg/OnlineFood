from django import forms
from .models import User,UserProfile
from .validators import allow_only_img

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
        

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'address','required':'required'}))
    profile_pic=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_img])
    cover_photo=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_img])
    #latitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    #longitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model = UserProfile
        fields = ['profile_pic','cover_photo','address','country','state','city','pin_code','latitude','longitude',]

    
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args,**kwargs)
        for field in self.fields:
            if field=='latitude' or field=='longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'