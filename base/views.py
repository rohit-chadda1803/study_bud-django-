from django.shortcuts import render , redirect

from django.http import HttpResponse

from .models import Room

from .forms import RoomForm

# rooms =[
   
#     {'id': 1, 'name': 'Lets Learn Python'},
#     {'id': 2, 'name': 'Python for Beginners'},
#     {'id': 3, 'name': 'Object-Oriented Python'},
#     {'id': 4, 'name': 'Python Data Structures'},
#     {'id': 5, 'name': 'Web Development with Django'},
#     {'id': 6, 'name': 'Flask Crash Course'},
#     {'id': 7, 'name': 'Automate with Python'},

# ] # used as temprory date before i created rroms model .

def home(request):
    # return HttpResponse("<h1>home working fine</h1>")

    # return render(request , 'home.html', {'rooms':rooms}  )// redirect to templates-->home.html . 
    rooms= Room.objects.all() 
    return render(request , 'base/home.html', {'rooms':rooms}  )

def room(request ,pk):
    # return HttpResponse("<h1>we will have rooms here</h1>")
     
    # room = None 
    # for i in rooms :
    #     if i['id'] == int(pk):
    #         room =i ; 

    room = Room.objects.get(id=pk)
    
    context = {'room':room}
    # return render(request , 'room.html' , {'rooms':rooms})
    
    return render(request , 'base/room.html' , context)


def createRoom(request):
    form = RoomForm

    if request.method == "POST" :
        # print(request.POST) 
        form = RoomForm(request.POST) # iss post se voo data lo jo roomform model ki key se match 
        if form.is_valid():
            form.save()  #save it in database 

            return redirect('home')
         
    context = {'form': form}
    return render(request , 'base/room_form.html' , context)


def updateRoom(request ,pk):
    room = Room.objects.get(id = pk)
    
    form = RoomForm(instance=room) #prefilled with room value . 
    
    if request.method == "POST" :
        # print(request.POST) 
        form = RoomForm(request.POST , instance=room) # ye room ka instance h , new room nhi bnana . 
        if form.is_valid():
            form.save()  #save it in database 

            return redirect('home')
        

    context = {'form':form}

    return render(request , 'base/room_form.html' , context)
