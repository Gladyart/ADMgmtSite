from django.db import models

# Create your models here.

class User(models.Model):
    accountExpires = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    displayName = models.CharField(max_length=20)
    lastLogon = models.CharField(max_length=20)
    mail = models.EmailField(max_length=100)
    manager = models.CharField(max_length=20)
    pwdLastSet = models.CharField(max_length=20)
    sAMAccountName = models.CharField(max_length=20)

    def __str__(self):
        return self.sAMAccountName


class Group(models.Model):
    pass