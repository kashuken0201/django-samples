from django import forms
from .models import Facilities, Room

class FacilitiesForm(forms.ModelForm):
    facility_name = forms.CharField(
        label='Facilities Name',
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Facilities name here'
            }
        )
    )
    quantity = forms.CharField(
        label='Quantity',
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Quantity',
            }
        )
    )

    class Meta:
        model = Facilities
        fields = [
            'facility_name',
            'quantity',
            'room'
        ]

        def __init__(self, *args, **kwargs) -> None:
            super(FacilitiesForm, self).__init__(*args, **kwargs)

            room = Room.objects.all()
            rooms = [(i.id, i.room_name) for i in room]
            self.fields['room'].choices = rooms
