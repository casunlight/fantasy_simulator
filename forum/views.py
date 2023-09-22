from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm

# Create your views here.

#queryset = Model.objects.all()
#variableThatHoldsResponse=Model.ModelObjectManager.method()
#other methods: get(), filter(), exclude(). all() and exclude() return all objects, get() just one

""" rooms = [
    {'id':1, 'name': 'Main'},
    {'id':2, 'name': 'Lets learn Fantasy'},
    {'id':3, 'name': 'Blurbs/Thoughts'},
    {'id':4, 'name': 'Optimizer questions'},
] """
#shift+option+A


def forum_home(request):
    rooms = Room.objects.all()#def objects(cls: Type[_M]) -> BaseManager  #def all(self: _QS) -> _QS: ...
    context = {'rooms': rooms}
    return render(request, 'forum/forum_home.html', context)

def forum_room(request, pk):
    room=Room.objects.get(id=pk)
    #for i in rooms:
    #    if i['id']==int(pk):
    #        room=i
    #context dict, a dict within a dict
    context={'room': room}
    return render(request, 'forum/forum_room.html', context)


def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        print(request.POST)#not sure what this does
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum_home')


    context = {'form': form}
    return render(request, 'forum/room_form.html', context)


def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('forum_home')


    context = {'form': form}
    return render(request, 'forum/room_form.html', context)

