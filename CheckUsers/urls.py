from django.urls import path, include
from allauth.account.views import LogoutView,password_reset
from . import views
import book_testing

urlpatterns = [
    # path('', index, name=''),
    # path('',index,name='home'),
    path('abc/', book_testing.views.index, name='index'),
    # path('home' , index, name='home'),
    # path('signup' ,signupView.as_view(), name='signup'),
    path('logins' , views.index, name='logins'),
    # path('logout' , LogoutView.as_view(),name='logout'),
]