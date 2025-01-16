from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .ldap import DCConnection, ADUser, OUPath, userAttributes

conn = DCConnection.conn
currentUser = 'gladyart'

def index(response):
    return render(response, "base.html")
        
def home(request):
            
    if request.method == "POST":
        searched = request.POST["searched"]

        searchParameters = f'(&(objectclass=person)(cn=*{searched}*))'        
        conn.search(OUPath, searchParameters, attributes=['sAMAccountName'])                       
        searched = conn.entries

        if not searched:
            messages.success(request, "Item not found")
            return render(request, "search.html", {})
        else:
            return render(request, "search.html", {"searched":searched})
    else:
        
        searchParameters = f'(&(objectclass=person)(cn={currentUser}))'                    
        entry = conn.entries[0]

        return render(request, "home.html", {"entry":entry})


def search(request):

    if request.method == "POST":       
        searched = request.POST["searched"]

        if not searched:
            messages.success(request, "Item not found")
            return render(request, "search.html", {})
        else:
            searchParameters = f'(&(objectclass=person)(cn=*{searched}*))'
            conn.search(OUPath, searchParameters, attributes=['sAMAccountName'])                       
            searched = conn.entries

            return render(request, "search.html", {"searched":searched})
    
    else:
        return render(request, "search.html", {})


def userID(response, id):

    entry = ADUser(id)
    ADUser.lockoutStatusCheck(entry, id)
   
    return render(response, "AD_user.html", {"entry":entry})

