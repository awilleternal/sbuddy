from django.forms import ModelForm
from .models import Room,message 
class RoomForm(ModelForm):
    
    class Meta:
        model = Room
        fields = '__all__'
class messageForm(ModelForm):
    class Meta:
        model=message
        fields=['body']
