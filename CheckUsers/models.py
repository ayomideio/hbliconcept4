import random

from django.db import models

# Create your models here.

class IC4_Users(models.Model):
    class Meta:
        db_table='IC4_PRO_USERS'
    USR_KEY =models.IntegerField(null=True, blank=True)
    USER_ID =  models.CharField(primary_key=True,max_length=200)
    USER_EMAIL =  models.EmailField(max_length=100)
    USER_PWD =  models.CharField(max_length=245)
    FIRST_NAME = models.CharField(max_length=200)
    MIDDLE_NAME = models.CharField(max_length=200)
    LAST_NAME = models.CharField(max_length=200)
    BRANCH_CODE = models.CharField(max_length=20)
    PASSWORD_EXPIRY_DATE = models.DateTimeField(null=True, blank=True)
    BLOCKED_UNTIL_DATE =  models.DateTimeField(null=True, blank=True)
    CREATION_DATE = models.DateTimeField(null=True, blank=True)
    MODIFICATION_DATE = models.DateTimeField(null=True, blank=True)
    STATUS = models.CharField(max_length=100, default=None, null=True, blank=True)
    USER_COMMENT = models.CharField(max_length=500,default=None, null=True, blank=True)
    USE_ALL_BRANCHES =models.BooleanField(default=False)

    TRUSTED =models.BooleanField(default=False)
    GRADE_LEVEL = models.CharField(max_length=200)
    LANG_KEY = models.CharField(max_length=20)

    USER_ID_ALIAS = models.CharField(max_length=200)
    USER_ROLE = models.CharField(max_length=200)

    LDAP_USER_ID = models.CharField(max_length=200)
    

    class User_Branches(models.Model):
        class Meta:
            db_table='USER_BRANCHES'
        id = models.CharField(primary_key=True,max_length=20)
        USER_ID=models.CharField(max_length=20)
        BRANCH_CODE=models.CharField(max_length=20)

   