from django.contrib import admin
from .models import *
from django_reverse_admin import ReverseModelAdmin

# Register your models here.
# class RoleAdmin(admin.ModelAdmin):
#     list_display = ('Group_Id','Menu_Name','Add','Edit','Delete')



# class GroupAdmin(admin.ModelAdmin):
#     list_display = ('Group_Id','Group_Name','Description')



# admin.site.register(Group,GroupAdmin)
# admin.site.register(Role,RoleAdmin) 