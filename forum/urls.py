from django.urls import path
from . import views#from this folder import views

urlpatterns = [
    path('', views.forum_home, name='forum_home'),
    path('room/<str:pk>/', views.forum_room, name='forum_room'),
    path('create-room/', views.createRoom, name='create_room'),
    path('update-room/<str:pk>/', views.updateRoom, name='update_room'),
]

#https://www.youtube.com/watch?v=PtQiiknWUcI&t=3153s&ab_channel=TraversyMedia
#min 59, says can use str or int ... pk means primary key
#must pass in a parameter to views.forum_room which you are calling
