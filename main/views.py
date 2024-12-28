from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .ldap import DCConnection

conn = DCConnection.conn
OUPath = DCConnection.OUPath
userAttributes = ['accountExpires', 'description', 'displayName', 'distinguishedName', 'lastLogon', 'mail', 'manager', 'pwdLastSet', 'sAMAccountName']

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
        currentUser = 'gladyart'
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
    
    userID = id

    searchParameters = f'(&(objectclass=person)(cn={userID}))'

    conn.search(OUPath, searchParameters, userAttributes)
        
    entry = conn.entries[0]
   
    return render(response, "home.html", {"entry":entry})

