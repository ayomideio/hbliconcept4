from django.urls import path #register_converter
# from datetime import datetime
from . import views
from django.conf import settings
from django.conf.urls.static import static
# class DateConverter:
#     regex = '\d{4}-\d{2}-\d{2}'

#     def to_python(self, value):
#         return datetime.strptime(value, '%Y-%m-%d')

#     def to_url(self, value):
#         return value

# register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('manual_exception/<callover_id>', views.Exception_Detail, name='manual_exception'),

    path('index', views.indexall, name='manualexception'),
    path('indexfrommail/<calloverid>', views.clickfromMail, name='clickmanualexceptionfrommailreview'),
    path('indexofcreate', views.Followup_Detail, name='manualexceptiondetail'),
    path('acceptmanualexception/', views.CreateManualException, name='manualexception_acceptreview'),
    path('editmanualexception/', views.EditManualException, name='editmanualexception'),
    path('observation/', views.Observation, name="Observation")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)