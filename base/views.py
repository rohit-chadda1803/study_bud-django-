from django.shortcuts import render , redirect

from django.http import HttpResponse

from .models import Room ,Topic , Message

from .forms import RoomForm  

from django.db.models import Q # for complex queries .

from django.contrib.auth.models import User

from django.contrib import messages

from django.contrib.auth import login , logout , authenticate

from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm # for creating user in register page .

# rooms =[
   
#     {'id': 1, 'name': 'Lets Learn Python'},
#     {'id': 2, 'name': 'Python for Beginners'},
#     {'id': 3, 'name': 'Object-Oriented Python'},
#     {'id': 4, 'name': 'Python Data Structures'},
#     {'id': 5, 'name': 'Web Development with Django'},
#     {'id': 6, 'name': 'Flask Crash Course'},
#     {'id': 7, 'name': 'Automate with Python'},

# ] # used as temprory date before i created rroms model .

def loginPage(request):
    page='login'

    if request.user.is_authenticated: # if user is already logged in then redirect to home page .
        return redirect('home')
    
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # print(username ,"" , password) # to check what is being passed in post request .

        try: 
            user = User.objects.get(username=username)# get user from database with this usename.
        except:
            messages.error(request, "User not found") # if user not found then show this error .

        user = authenticate(request , username=username, password=password) # authenticate user with username and password .

        if user is not None: 
            login(request,user)
            return redirect('home')
        
        else:
           messages.error(request, "Username or password not exist ")

    context = {'page':page} # to check which page is being rendered login/register.

    return render(request , 'base/login_register.html',context) 

def logoutUser(request):
    logout(request)
    return redirect('home')


def registerPage(request):
  
   form = UserCreationForm() # to create user in register page .

   if request.method == 'POST':
       form = UserCreationForm(request.POST)
       if form.is_valid():
          user= form.save(commit=False) # commit=False means don't save it in database yet , we will do it later .
          user.username = user.username.lower()
          user.save()
          
          login(request,user)
          
          return redirect('home')
       else:
           messages.error(request , "An error has occurred during registration") # if form is not valid then show this error .
   
   return render(request , 'base/login_register.html', {'form':form})



def home(request):
    # return HttpResponse("<h1>home working fine</h1>")

    # return render(request , 'home.html', {'rooms':rooms}  )// redirect to templates-->home.html . 

    q=request.GET.get('q') if request.GET.get('q')!=None else ''
    # rooms= Room.objects.all() 
    
    if q=='':
        rooms =Room.objects.all()
        room_messages=Message.objects.all() ; 
    else :
    #    rooms=Room.objects.filter(topic__name__icontains=q)
    #     #__icontains make it case insensitive & half name after 'q=' also vallid , like for q=w it will understand it as q=web%20dev i.e best available topic for autocomplete. 

        rooms = Room.objects.filter(
            Q(topic__name__icontains=q) | 
            Q(description__icontains=q) |
            Q(name__icontains=q)
        )

        room_messages = Message.objects.filter(
            Q(room__name__icontains=q) |
            Q(room__topic__name__icontains=q) |
            Q(body__icontains=q) 
        )

       
    topics=Topic.objects.all() 
    
    rooms_count = rooms.count() 

   

    context = {'rooms':rooms , 'topics':topics , 'rooms_count':rooms_count , 'room_messages':room_messages}
    return render(request , 'base/home.html', context  )

def room(request ,pk):
    # return HttpResponse("<h1>we will have rooms here</h1>") 
    # room = None 
    # for i in rooms :
    #     if i['id'] == int(pk):
    #         room =i ; 

    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created') # get all messages related to this room .
    participants = room.participants.all() # get all participants of this room .
    if request.method == "POST":
        body = request.POST.get('body') # get the body of message from post request .
        
        if body != '' :
          message  = Message.objects.create(
              user = request.user, 
              room =room , 
              body=body 
          )
          room.participants.add(request.user) # add user to participants of this room .
          return redirect('room',pk=room.id) # without it ,  work well , lekin isse hm ensure krre ki koi Get wala form ho , ya koi aur issue , i dont care , phir se ye page load krke do , bilkul fresh.  

    # print(room_messages) # to check if messages are being fetched or not .
    
    context = {'room':room , 'room_messages':room_messages , 'participants':participants} # pass room and messages to template .
    
    # return render(request , 'room.html' , {'rooms':rooms})
    
    return render(request , 'base/room.html' , context)

@login_required(login_url='login')

def createRoom(request):
    form = RoomForm

    if request.method == "POST" :
        # print(request.POST) 
        form = RoomForm(request.POST) # iss post se voo data lo jo roomform model ki key se match. 
        if form.is_valid():
            form.save()  #save it in database 

            return redirect('home')
         
    context = {'form': form}
    return render(request , 'base/room_form.html' , context)


@login_required(login_url='login')
def updateRoom(request ,pk):
    room = Room.objects.get(id = pk)
    
    form = RoomForm(instance=room) #prefilled with room value . 
    
    if request.user != room.host:
        return HttpResponse("You are not allowed here !  Only writer can update the content of room ")

    if request.method == "POST" :
        # print(request.POST) 
        form = RoomForm(request.POST , instance=room) # ye room ka instance h , new room nhi bnana . 
        if form.is_valid():
            form.save()  #save it in database 

            return redirect('home')
        

    context = {'form':form}

    return render(request , 'base/room_form.html' , context)

@login_required(login_url='login')
def deleteroom(request ,pk):
    room=Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse("You are not allowed here !  Only writer can update the content of room ")

    if request.method=='POST':
        room.delete() #to delete item from database . 
        return redirect('home')
    return render(request , 'base/delete.html',{'obj':room})


@login_required(login_url='login')
def deleteMessage(request ,pk):
    message=Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse("You are not allowed here !  Only writer can update the content of room ")

    if request.method=='POST':
        message.delete() #to delete item from database . 
        return redirect('home')
    return render(request , 'base/delete.html',{'obj':message})