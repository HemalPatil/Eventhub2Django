from django import forms
from django.forms import widgets
from django.forms import ModelForm
from django.contrib.auth.models import User
from authentication.models import UserProfile
from django.contrib import admin

class UserForm( forms.ModelForm ):
    password=forms.CharField()
    class Meta:
        model= User
        exclude= ('email','last_login','date_joined',)
    username = forms.EmailField(max_length=64,
        help_text = "The person's email address.")
    def clean_email( self ):
        email= self.cleaned_data['username']
        return email

admin.site.unregister( User )
admin.site.register( User)

class UserProfileForm(ModelForm):
	"""form for extended auth User model"""
	class Meta:
		model = UserProfile
		exclude=('signUpDate','ipaddress','lastLoginDate','collegeName','loggedIn')