from django import forms
from rental.models import RegisteredUser
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    phone = forms.CharField()

    class Meta:
        model = RegisteredUser
        fields = ('phone', 'login', 'email', 'password1', 'password2',)

