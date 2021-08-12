from django.http import HttpResponseRedirect
from django.shortcuts import render
from allauth.account.views import SignupView, LoginView, PasswordResetView, PasswordResetDoneView
from CheckComp.forms import CustomSignupForm, CustomLoginForm
from .models import IC4_Users



# class loginView(LoginView):
#     template_name = 'allauth/account/login.html'
#     form_class = CustomLoginForm()


# class signupView(SignupView):
#     template_name = 'allauth/account/signup.html'
#     form_class = CustomSignupForm()

def login(request):
    return render(request,'allauth/account/login.html')



def index(request):
    if request.is_ajax and request.method == "POST":
        USER_ID = request.POST['userid']
        c4user = IC4_Users.objects.get(pk=USER_ID)

        userid = request.POST['userid']
     
        password = request.POST['password']
      
    # if c4user.USER_ID:
    #     return render(request, 'book/library.html', {"": ""})
    
    
    

          


    # return HttpResponse(True)

