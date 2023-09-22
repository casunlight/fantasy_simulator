"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""


from django.contrib import admin
from django.urls import path
from django.urls import include
from django.http import HttpResponse
from django.shortcuts import render

#If you are seeing errors here, it's prob because your VS CODE interpreter isn't linked to your virtual env where you installed django


#Need all url patterns in here even for other apps

#https://www.youtube.com/watch?v=PtQiiknWUcI&t=2149s&ab_channel=TraversyMedia  min32
def home(request):
    #request object will give all the info the user sent from his/her request
    return render(request, 'home.html')

def about(request):
    #request object will give all the info the user sent from his/her request
    return render(request, 'about.html')


urlpatterns = [
    path('',home),
    path('admin/', admin.site.urls),
    path('about/', about),
    path('api/',include('api.urls')),
    path('golf/', include('golf.urls')),
    path('nfl/', include('nfl.urls')),
    path('nba/', include('nba.urls')),
    path('mlb/', include('mlb.urls')),
    path('forum/', include('forum.urls')),
]

#variables are represented with {{}} in django templating engine, passed in via a dictionary object 'var': my_var --> {{var}}