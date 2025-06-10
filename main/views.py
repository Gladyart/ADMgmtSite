from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .ldap import DCConnection, ADUser, OUPath, conn


currentUser = 'Admin'

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
            return render(request, "search.html", {"currentUser":currentUser})
        else:
            return render(request, "search.html", {"searched":searched, "currentUser":currentUser})
    else:
        
        searchParameters = f'(&(objectclass=person)(cn={currentUser}))'                    
        entry = conn.entries[0]

        return render(request, "home.html", {"entry":entry, "currentUser":currentUser})


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

            return render(request, "search.html", {"searched":searched, "currentUser":currentUser})
    
    else:
        return render(request, "search.html", {"currentUser":currentUser})


def userID(request, id):

    entry = ADUser(id)

    method = request.GET.get('method')
    if method == 'method1':            
        ADUser.enableUser(entry)
        return HttpResponseRedirect(reverse('userID', args=(entry.sAMAccountName)))
    elif method == 'method2':            
        ADUser.disableUser(entry)
        return HttpResponseRedirect(reverse('userID', args=(entry.sAMAccountName)))
    elif method == 'method3':        
        pass
    elif method == 'method4':
        ADUser.unlockUser(entry)
    elif method == None:
        pass
        
   
    return render(request, "AD_user.html", {"entry":entry, "currentUser":currentUser})

