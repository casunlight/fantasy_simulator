#Can add a urls.py for each app

from django.urls import path
from . import views#from this folder import views

urlpatterns = [
    path('', views.golf, name='golf')
]

#dont double count slate .. already have slate in the root urls file