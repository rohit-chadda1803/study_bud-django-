from django.urls import path

from . import views


from django.http import HttpResponse

def extra(request):
    return  HttpResponse("this is extra for which func in urls . ")

urlpatterns=[
    path('' ,views.home , name="home"),
    path('room/<str:pk>/' , views.room , name="room") , 
    path('create-room/' ,views.createRoom  , name = "create-room") ,
    path('update-room/<str:pk>' ,views.updateRoom  , name = "update-room") ,
    
    path('extra/',extra) , #it proves func can in in views / or even in urls.py
    

]