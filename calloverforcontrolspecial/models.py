from django.db import models
from django.utils import timezone
# Create your models here.

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

