from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your username here'
            }
        )
    )
    password = forms.CharField(
        label='Password:',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your password here'
            }
        )
    )

    class Meta:
        model = Account
        fields = ['username', 'password']

class ProfileForm(forms.Form):
    class Meta:
        model = Account
        fields = [
            'fullname',
            'email',
            'avatar', 
            'phone', 
            'age']

    fullname = forms.CharField(
        label='Full name:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your name here'
            }
        )
    )

    email = forms.EmailField(
        label='Email:',
        required=False,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your email here'
            }
        )
    )

    avatar = forms.ImageField(
        label='Avatar:',
        required=False,
        allow_empty_file=True,
    )

    phone = forms.CharField(
        label='Phone:',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your phone here'
            }
        )
    )
    age = forms.IntegerField(
        label='Age:',
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your age here'
            }
        )
    )