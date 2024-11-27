from django.forms import ModelForm
from .models import Room,message 
from django.contrib.auth.models import User
class RoomForm(ModelForm):
    
    class Meta:
        model = Room
        fields = '__all__'
        exclude=['host','participants']
class messageForm(ModelForm):
    class Meta:
        model=message
        fields=['body']

class userForm(ModelForm):
    class Meta:
        model=User
        fields=['username','email']
        
