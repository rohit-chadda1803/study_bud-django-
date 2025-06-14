from django.urls import path

from . import views


from django.http import HttpResponse

def extra(request):
    return  HttpResponse("this is extra for which func in urls . ")

urlpatterns=[
    path('login/' , views.loginPage,name = 'login') , 
    path('register/' , views.registerPage,name = 'register') , 
    path('logout/' , views.logoutUser , name = 'logout') ,
    path('' ,views.home , name="home"),
    path('room/<str:pk>/' , views.room , name="room") , 
    path('delete-message/<str:pk>/' ,views.deleteMessage , name='delete-message'), 
    path('create-room/' ,views.createRoom  , name = "create-room") ,
    path('update-room/<str:pk>/' ,views.updateRoom  , name = "update-room") ,
    path('delete-room/<str:pk>/',views.deleteroom , name='delete-room'),

    path('extra/',extra) , #it proves func can in in views / or even in urls.py
    

]