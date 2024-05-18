from django.shortcuts import render
from django.http import HttpResponse
from .tests import DCConnection


def index(response):
    return render(response, "base.html")
def home(response):
    ls = DCConnection.ls

    return render(response, "home.html", {"ls":ls})