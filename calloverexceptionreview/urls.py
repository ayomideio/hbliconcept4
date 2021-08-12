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
    
    path('index', views.index, name='calloverexceptionreviewindex'),
    path('calloverexception/<callover_id>', views.Exception_Detail, name='calloverexceptionreview'),
    path('calloverexceptionfrommail/<calloverid>', views.clickfromMail, name='clickfrommailreview'),
    path('acceptreview', views.Accept, name='calloverexceptionreview_acceptreview'),
    
]