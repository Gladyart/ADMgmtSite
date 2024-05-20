from django.db import models

# Create your models here.

class User(models.Model):
    accountExpires = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    displayName = models.CharField(max_length=20)
    lastLogon = models.CharField(max_length=20)
    mail = models.CharField(max_length=20)
    manager = models.CharField(max_length=20)
    objectclass = models.CharField(max_length=20)
    pwdLastSet = models.CharField(max_length=20)
    sAMAccountName = models.CharField(max_length=20)


class Group(models.Model):
    pass