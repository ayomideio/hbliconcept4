from django.http import HttpResponseRedirect,HttpResponse,HttpResponseRedirect
from django.shortcuts import render
from allauth.account.views import SignupView, LoginView, PasswordResetView, PasswordResetDoneView
from CheckComp.forms import CustomSignupForm, CustomLoginForm
from django.db import connection
from iconcept4.views import dictfetchall
from django.urls import reverse


# Create your views here.


class loginView(LoginView):
    template_name = 'allauth/account/login.html'
    form_class = CustomLoginForm()


class signupView(SignupView):
    template_name = 'allauth/account/signup.html'
    form_class = CustomSignupForm()


def index(request):
    print("here")
    cursor = connection.cursor()
    query=""" SELECT * FROM AUTH_USER  where username='adroit' and password=12345678 """
    c4user = cursor.execute(query)
    yList = dictfetchall(cursor)

    print(yList)
    return render(request, 'book/library.html', {"": ""})
