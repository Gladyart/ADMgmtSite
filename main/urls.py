from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("",  views.index, name="index"),
    path("home",  views.home, name="home"),
    path("search/",  views.search, name="search"),
    path("object/<str:id>",  views.userID, name="userID"),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    
]