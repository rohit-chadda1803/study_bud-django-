from django.forms import ModelForm
from .models import Room


class RoomForm(ModelForm):
    class Meta:
        model=Room
        fields='__all__'  # or write values in list to input in form ----> ['name' , 'topic' , -----]

