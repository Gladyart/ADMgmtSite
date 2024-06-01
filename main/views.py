from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .tests import DCConnection



def index(response):
    return render(response, "base.html")

def home(response):
    
    accountExpires = DCConnection.entry['accountExpires']
    description = DCConnection.entry['description']
    displayName = DCConnection.entry['displayName']
    lastLogon = DCConnection.entry['lastLogon']
    mail = DCConnection.entry['mail']
    manager = DCConnection.entry['manager']
    pwdLastSet = DCConnection.entry['pwdLastSet']
    sAMAccountName = DCConnection.entry['sAMAccountName']

    return render(response, "home.html", {"accountExpires":accountExpires,
                                          "description":description,
                                          "displayName":displayName,
                                          "lastLogon":lastLogon,
                                          "mail":mail,
                                          "manager":manager,
                                          "pwdLastSet":pwdLastSet,
                                          "sAMAccountName":sAMAccountName,
                                          })


def search(request):

    if request.method == "POST":
        searched = request.POST["searched"]
        
        conn = DCConnection.conn
        OUPath = DCConnection.OUPath

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

    conn = DCConnection.conn
    OUPath = DCConnection.OUPath

    searchParameters = f'(&(objectclass=person)(cn={userID}))'

    conn.search(OUPath, searchParameters, 
                attributes=['accountExpires', 'description', 'displayName','lastLogon', 'mail', 'manager', 'pwdLastSet', 'sAMAccountName'])
        
    entry = conn.entries[0]
   
    return render(response, "home.html", {"accountExpires":entry['accountExpires'],
                                          "description":entry['description'],
                                          "displayName":entry['displayName'],
                                          "lastLogon":entry['lastLogon'],
                                          "mail":entry['mail'],
                                          "manager":entry['manager'],
                                          "pwdLastSet":entry['pwdLastSet'],
                                          "sAMAccountName":entry['sAMAccountName'],
                                          })

