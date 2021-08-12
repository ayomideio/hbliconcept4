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
    
    path('index/<id>', views.index, name='alertreviewindex'),
    path('index', views.indexall, name='alertreviewindexall'),
    path('followindex', views.indexoffollow, name='followupindex'),
    path('followindexall', views.indexoffollowall, name='followupindexall'),
    path('follow/<callover_id>', views.Followup_Detail, name='followdetail'),
    path('alertreview/<callover_id>', views.Exception_Detail, name='alertreview'),
    path('alertreviewfrommail/<calloverid>', views.clickfromMail, name='clickalertreviewfrommailreview'),
    path('acceptalertreview', views.Accept, name='alertreview_acceptreview'),
    path('acceptfollowreview', views.AcceptFollow, name='followreview_acceptreview'),
    
]