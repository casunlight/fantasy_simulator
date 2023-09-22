from django.urls import path
from . import views#from this folder import views

urlpatterns = [
    path('', views.mlb, name='mlb')
]