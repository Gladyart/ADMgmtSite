from django.urls import path
from . import views

urlpatterns = [
    path("",  views.index, name="index"),
    path("home",  views.home, name="home"),
    path("search/",  views.search, name="search"),
    #path("<str:id>",  views.userID, name="userID"),
    
]