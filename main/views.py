from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .ldap import DCConnection, OUPath, userAttributes

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
        
        try:
            conn.search(OUPath, searchParameters, attributes=userAttributes)   
        except:
            conn.bind()
            conn.search(OUPath, searchParameters, attributes=userAttributes)                     
        entry = conn.entries[0]

        return render(request, "home.html", {"entry":entry})


def search(request):

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
        return render(request, "search.html", {})


def userID(response, id):

    entry = DCConnection.searchADPerson(userID=id, OUPath=OUPath, conn = DCConnection.conn)
   
    return render(response, "AD_user.html", {"entry":entry})

