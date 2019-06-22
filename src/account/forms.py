from django import forms
from django.contrib.auth.models import 	User
from django.forms import ValidationError
from .models import Profile



# a form to register the new user
class UserRegistrationForm(forms.ModelForm):
	password = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('username', 'first_name', 'email')

	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password']!=cd['password2']:
			raise forms.validationError("passwords don't match")
		return cd['password2']


# a form to let an existing user edit his user related details 
class UserEditForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name','last_name','email')


# a form to let an existing user edit his profile
class ProfileEditForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ('date_of_birth','photo')
