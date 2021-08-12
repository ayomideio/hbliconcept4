
from django.urls import path
from . import views

urlpatterns = [
    path('group/', views.group, name='group'),
    path('creategroup/',views.creategroup ,name='creategroup'),
    path('role/', views.role,name='getrole'),
    path('createrole/',views.createrole ,name='createrole'),
    path('editgroup/:<pk>)', views.editgroup, name='editgroup'),
    path('editrole/:<pk>)', views.editrole, name='editrole'),
    path('deleterole/:<pk>)', views.deleterole, name='deleterole'),
    path('deletegroup/:<pk>)', views.deletegroup, name='deletegroup'),
    path('userrole',views.userrole, name='userrole'),
    path('createuserrole',views.createuserrole, name='createuserrole'),
    path('edituserrole/:<pk>',views.edituserrole,name='edituserrole'),
    path('deleteuserrole/:<pk>',views.deleteuserrole,name='deleteuserrole')
    

]