from django.shortcuts import render

from django.http import HttpResponse

from .models import Room

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


# Create your views here.
