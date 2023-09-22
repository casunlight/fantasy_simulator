from django.shortcuts import render
from django.urls import path
from django.http import HttpResponse
import json

# Create your views here.
with open('slate_json/dk_pga_slate_classic.json', 'r') as file:
    slate_list = json.load(file)

nested_list=[]
for item in slate_list:
    nested_list.append(item['fields'])


def golf(request):
    return render(request, 'opto_table.html', {'slate_list': nested_list})