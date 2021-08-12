from django.urls import path, include
from allauth.account.views import LogoutView,password_reset
from .views import signupView, index
import iconcept4
from iconcept4.views import indexoflogin

urlpatterns = [
    # path('', index, name=''),
    path('',index,name='home'),
    path('abc/', iconcept4.views.index, name='index'),
    path('home' , index, name='home'),
    path('signup' ,signupView.as_view(), name='signup'),
    path('login' , indexoflogin, name='login'),
    path('logout' , LogoutView.as_view(),name='logout'),
]