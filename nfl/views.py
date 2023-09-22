from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
import json

# Create your views here.
with open('./slate_json/dk_nfl_main_slate.json', 'r') as file:
    slate_list = json.load(file)

nested_list=[]
for item in slate_list:
    nested_list.append(item['fields'])

def nfl(request):
    return render(request, 'base_opto.html', {'slate_list': nested_list})

