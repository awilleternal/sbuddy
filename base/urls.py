from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.loginp, name="login"),
    path("register/", views.reg, name="register"),
    path("logout/", views.logoutu, name="logout"),
    path('',views.home,name='home'),
    path('room/<str:pk>/',views.room,name='room'),
    path('profile/<str:pk>/',views.userProfile,name='user-profile'),
    path('create-room/',views.createRoom,name='create-room'),
    path('update-room/<str:pk>',views.updateRoom,name='update-room'),
    path('delete-room/<str:pk>',views.deleteRoom,name='delete-room'),
    path('delete-msg/<str:pk>',views.deleteMsg,name='delete-msg'),
    path('update-msg/<str:pk>',views.updateMsg,name='update-msg'),
    path('update-user/',views.updateUser,name='update-user'),

    
    
    
]
