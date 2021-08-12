from django.shortcuts import render
import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.http import HttpResponse,HttpResponseRedirect
from userapp.models import Groupss, Roless,Ic4_Menus
# from .queries import *
from django.db import connection
from .models import Groupss,Roless,UserRoles
from .forms import GroupCreate,RoleCreate
from django.urls import reverse
from iconcept4.views import dictfetchall
from django.db import connection


# Create your views here.
def group(request):
    # query = group_query()
    # cursor = connection.cursor()
    # result = cursor.execute(query, None)
    model=Groupss
    group=Groupss.objects.all()
   
       
    
    return render(request, 'IC4_Group.html', {'group': group})

def userrole(request):
    query=""" SELECT * FROM IC4_PRO_USERS """
    cursor = connection.cursor()
    cursor.execute(query)
    yList = dictfetchall(cursor)
    # print(yList)
    return render(request,'userrole.html',{'cont':yList,'group':Groupss.objects.all(),'userrole':UserRoles.objects.all()})
# def edituserrole(request,pk=None):
#     if (request.method=='POST'):
#         UserRole.objects.filter(pk=)
def createuserrole(request):
    if (request.method=='POST'):
        User_Id=request.POST.get('name')
        Group_Name=request.POST.get('email')
        createnew=UserRoles(User_Id=User_Id,Group_Name=Group_Name)
        createnew.save()
        return HttpResponseRedirect(reverse('userrole'))
def edituserrole(request,pk=None):
    print(pk)
    if(request.method=='POST'):
        UserRoles.objects.filter(pk=request.POST.get('name2')).update(Group_Name=request.POST.get('email2'))
        return HttpResponseRedirect(reverse('userrole'))
def deleteuserrole(request,pk=None):
    deluserrolee=UserRoles.objects.get(pk=request.POST.get('name3'))
    deluserrolee.delete()
    return HttpResponseRedirect(reverse('userrole'))
def creategroup(request):
    create=GroupCreate()
    if (request.method=='POST'):
        # create=GroupCreate(request.POST,request.Files)
        
           
        Group_Name=request.POST.get('name')
        Group_Id=request.POST.get('id')
        Description=request.POST.get('email')
        create_new=Groupss(Group_Id=Group_Name,Group_Name=Group_Id,Description=Description)
        create_new.save()
           
        
        return HttpResponseRedirect(reverse('group'))
def editgroup(request, pk=None):
    if (request.method=='POST'):
        print("ayomide")
        print(request.POST.get('name3'))
        print(request.POST.get('email2'))
        Groupss.objects.filter(pk=request.POST.get('name4')).update(Description=request.POST.get('email2'), Group_Name=request.POST.get('id4'))
        return HttpResponseRedirect(reverse('group'))

def deletegroup(request,pk=None):
    print(request.POST.get('name3'))
    delgroup=Groupss.objects.get(pk=request.POST.get('name3'))
    if (request.method=='POST'):
        delgroup.delete()
        return HttpResponseRedirect(reverse('group'))
  
def role(request):
    # query = role_query()
    # cursor = connection.cursor()
    # result = cursor.execute(query, None)
    ct={
        'role':Roless.objects.all(),
        'group':Groupss.objects.all(),
        'menu':Ic4_Menus.objects.all()
    }
    # role=Role.objects.all()

    return render(request, 'IC4_Role.html',ct)


def createrole(request): 
    create=RoleCreate()
    if (request.method=='POST'):   

        Group_Name=request.POST.get('groupname')
        Menu_Name=request.POST.get('rolename')
        Add=request.POST.get('addaction')
        Edit=request.POST.get('editaction')
        Delete=request.POST.get('deleteaction')
        if (Add=='Yes'):
            Add='Yes'
        else:
            Add='No'
        if (Edit=='Yes'):
            Edit='Yes'
        else:
            Edit='No'
        if (Delete=='Yes'):
            Delete='Yes'
        else:
            Delete='No'
        
        
        create_new=Roless(Group_Id=Groupss.objects.get(Group_Id=Group_Name),Menu_Name=Menu_Name,Add=Add,Edit=Edit,Delete=Delete)
        create_new.save()
           
        
        return HttpResponseRedirect(reverse('getrole'))

def editrole(request, pk=None):
    print(request.POST.get('groupname2'))
    Add=request.POST.get('addaction2')
    Edit=request.POST.get('editaction2')
    Delete=request.POST.get('deleteaction2')
    if (Add=='Yes'):
        Add='Yes'
    else:
        Add='No'
    if (Edit=='Yes'):
        Edit='Yes'
    else:
        Edit='No'
    if (Delete=='Yes'):
        Delete='Yes'
    else:
        Delete='No'
    if (request.method=='POST'):
        Roless.objects.filter(pk=1).update(Group_Id=Groupss.objects.get(Group_Id=request.POST.get('groupname2')),Add=Add,Edit=Edit,Delete=Delete,Menu_Name=request.POST.get('userrole2'))
        return HttpResponseRedirect(reverse('getrole'))

def deleterole(request,pk=None):
    delrole=Roless.objects.get(pk=request.POST.get('userrole3'))
    if (request.method=='POST'):
        delrole.delete()
        return HttpResponseRedirect(reverse('getrole'))
  