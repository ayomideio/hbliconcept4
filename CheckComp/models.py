from allauth.account.signals import user_signed_up
from django.db import models

# Create your models here.
from django.dispatch import receiver
from django.http import HttpResponseRedirect

#
# @receiver(user_signed_up, dispatch_uid="some.unique.string.id.for.allauth.user_signed_up")
# def user_signed_up_(request, user, **kwargs):
#     return HttpResponseRedirect('/account/login')
