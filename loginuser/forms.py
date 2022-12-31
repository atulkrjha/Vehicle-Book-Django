from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from django import forms


class RegisterUserForm(forms.ModelForm):	

	class Meta:
		model = User
		fields = ("email", "password")

class RegisterUserOtpForm(forms.ModelForm):	

	class Meta:
		model = User
		fields = ("otp",)




