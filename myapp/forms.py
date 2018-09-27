from django import forms
from django.contrib.auth.forms import UserCreationForm
#from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

class RegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=False)
    middle_name = forms.CharField(max_length=20, required=False, help_text='20 Characters.')
    phone = forms.CharField(max_length=12, required=False)

    class Meta:
        model = User
        fields = ('name', 'middle_name', 'phone', 'password1', 'password2', )

