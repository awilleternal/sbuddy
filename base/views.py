from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q
from .models import Room,Topic,message
from .forms import RoomForm,messageForm
# Create your views here.
# rooms=[
#     {'id':1,'name':'z'},
#     {'id':2,'name':'zf'},
#     {'id':3,'name':'zs'},
# ]

def loginp(request):
    page='login'
    
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=='POST':
        username=request.POST.get('username').lower()
        password=request.POST.get('password')
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request, "user not found.")
            
        user=authenticate(request,username=username,password=password)
        if user !=None:
            login(request,user)
        
            return redirect('home')
        else:
             messages.error(request, "user or passsdoes not exist")  
    return render(request,'base/login_reg.html',{'page':page})
def reg(request):
    form=UserCreationForm()
    if request.method =='POST':
        
        form =UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"somthioing went wrong")
        
        
    return render(request,'base/login_reg.html',{'form':form})
@login_required(login_url='login')
def logoutu(request):
    logout(request)
    return redirect('home')
def home(request):#req object is http object what is user sending to bacend
    rooms=Room.objects.all()
    q=request.GET.get('q') if request.GET.get('q') != None else ''
    #Q allows us to do to perform & and | on qurries bscially it searches query avaliABE IN EVERYTHING
    rooms=Room.objects.filter(Q(topic__name__icontains=q)
                              |Q(name__icontains=q) |  Q(description__icontains=q))#this finds __name refers to first it goes to room.topic then it goes to topic.name thsi does it by applying join internally on room and table  
    topics=Topic.objects.all()
    room_messages=message.objects.filter(Q(room__topic__name__icontains=q))
    r_c=rooms.count()
    context={'rooms':rooms,'topics':topics,'r_c':r_c,'room_messages':room_messages}
    return render(request,'base/home.html',context)
    
def room(request,pk):
    room=Room.objects.get(id=pk)
    room_messages=room.message_set.all().order_by('-created')#this give childeren of room tabel that is message table and all of these entrier in message table 
    participants=room.participants.all()
    if request.method== 'POST':
        msg=message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')  
        )
        room.participants.add(request.user)
        return redirect('room',pk=room.id ) 
        
            
        
    return render(request,'base/room.html',{'room':room,'room_messages':room_messages,'participants':participants})   

def userProfile(request,pk):
    user=User.objects.get(id=pk)
    room_messages=user.message_set.all()
    rooms=user.room_set.all()
    topics=Topic.objects.all()
    context={'user':user,'rooms':rooms,'room_messages':room_messages,'topics':topics}
    return render(request,'base/profile.html',context) 

@login_required(login_url='login')
def createRoom(request):
    
    form=RoomForm()
    if request.method == 'POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            room=form.save(commit=False)
            room.host=request.user
            room.save()
            return redirect('home')
            
    context={'form':form}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')
def updateRoom(request,pk):
    room=Room.objects.get(id=pk)
    form =RoomForm(instance=room)
    if request.user != room.host:
        return HttpResponse("you are not user")
        
    if request.method == 'POST':
        form=RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)
@login_required(login_url='login')       
def deleteRoom(request,pk):
    room=Room.objects.get(id=pk)
    if request.user != room.host:
        return HttpResponse("you are not user")
    if request.method =='POST':
        room.delete()
        return redirect('home')
    
    return render(request,'base/delete.html',{'obj':room})

def deleteMsg(request,pk):
    
    msg=message.objects.get(id=pk)
    room=msg.room
    if request.user != msg.user:
        return HttpResponse("you are not user")
    if request.method =='POST':
        msg.delete()
        user_in_room=message.objects.filter(room=room,user=msg.user).exists()
        if not user_in_room:
            room.participants.remove(msg.user)
        
        return redirect('home')
    
    return render(request,'base/delete.html',{'obj':msg})
    
def updateMsg(request,pk):
    room=message.objects.get(id=pk)
    form =messageForm(instance=room)
    if request.user != room.user:
        return HttpResponse("you are not user")
        
    if request.method == 'POST':
        form=messageForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context={'form':form}
    return render(request,'base/room_form.html',context)