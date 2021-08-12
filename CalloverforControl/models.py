from django.db import models
from django.utils import timezone

LCY_Codes = (
    ('USD', 'USD'),
    ('NGN', 'NGN'),
)
Trans_Choices = (
    ('Credit', 'CREDIT'),
    ('Debit', 'DEBIT'),
)
Trans_Codes = (
    ('Credit','C'),
    ('Debit','D')
)
# Create your models here.


