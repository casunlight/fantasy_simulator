from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse

# Create your views here.




def nba(request):
    return render(request, 'base_opto.html')


