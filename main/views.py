from django.shortcuts import render
from django.http import HttpResponse
from .tests import DCConnection
from .models import User


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
