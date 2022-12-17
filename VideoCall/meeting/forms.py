from django import forms
from .models import *

class RoomForm(forms.ModelForm):
    name = forms.CharField(
        label='Room name:',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Your room name here'
            }
        )
    )
    password = forms.CharField(
        label='Password:',
        required=False,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter a password here',
            }
        )
    )

    class Meta:
        model = Room
        fields = [
            'name',
            'password']