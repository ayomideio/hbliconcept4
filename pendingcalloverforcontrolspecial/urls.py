from django.urls import path #register_converter
# from datetime import datetime
from . import views

# class DateConverter:
#     regex = '\d{4}-\d{2}-\d{2}'

#     def to_python(self, value):
#         return datetime.strptime(value, '%Y-%m-%d')

#     def to_url(self, value):
#         return value

# register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('pendingcalloverforcontrolspecial_submit_exception/', views.Exceptions, name="pendingcalloverforcontrolspecialsubmit_exception"),
    path('acc_trans/pendingcalloverforcontrolspecial/ocr/', views.OCR, name="pendingcalloverforcontrolspecialOCR"),
    path('index', views.index, name='pendingcalloverforcontrolspecial_index'),
    path('bank_trans/<branch_id>', views.Bank_Trans, name='pendingcalloverforcontrolspecial_bank_trans'),
    path('acc_trans/<trans_id>', views.acc_trans, name='pendingcalloverforcontrolspecial_acc_trans'),

 
]