from django import forms
from .models import Groupss
from django.db import models


class GroupCreate(forms.Form):
    Group_Name = models.CharField()
    Description = models.TextField()

class RoleCreate(forms.Form):
    ID = models.AutoField()
    Group_Id = models.ForeignKey(Groupss, on_delete=models.CASCADE)
    Menu_Name = models.CharField()
    Add = models.BooleanField()
    Edit = models.BooleanField()
    Delete = models.BooleanField()