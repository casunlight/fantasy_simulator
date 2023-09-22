from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def getData(response):
    person = {'name': 'Dennis', 'Age': 28}
    mylist=[1,2,3,4]
    return Response(mylist)#Response always return its input as json data. What would a function look like in json?



