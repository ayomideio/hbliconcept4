from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class EmployeeeName(models.Model):

    # class Meta:
    #     db_table = "employee"

class Ic4_Menus(models.Model):
    class Meta:
        db_table='ic4_menus'
    menu_id=models.CharField(primary_key=True,max_length=100)
    menu_name=models.CharField(max_length=100)

class Groupss(models.Model):
    class Meta:
        db_table='Usergroup'
    Group_Id = models.CharField(primary_key=True, max_length=100)
    Group_Name = models.TextField()
    Description = models.TextField()

    def __str__(self):
        return self.Group_Id

class UserRoles(models.Model):
    class Meta:
        
        db_table="UserRole"
    
    User_Id=models.CharField(max_length=100,primary_key=True)
    Group_Name=models.CharField(max_length=100)


class Roless(models.Model):
    class Meta:
        db_table='Role'
    id=models.AutoField(primary_key=True)
    Group_Id = models.ForeignKey(Groupss, on_delete=models.CASCADE)
    Menu_Name = models.CharField(max_length=100)
    Add = models.CharField( max_length=100)
    Edit = models.CharField( max_length=100)
    Delete = models.CharField( max_length=100)
    # def __str__(self):
    #     return self.name