from django.shortcuts import render
from .models import ic4promenus
# Create your views here.
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseRedirect,JsonResponse
def index(request):
    data=ic4promenus.objects.all()
    args = {           
            'response': data,
                    
        }
    return JsonResponse(args)