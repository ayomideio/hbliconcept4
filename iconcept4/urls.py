"""book_testing URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from . import views

from django.views.static import serve
from django.conf import settings


from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns





urlpatterns = [    
    path('togoback/', views.togobacktologin, name='togobacktologin'),   
    path('abc/', views.index, name='index'),
    
    path('alert_review/',include("alert_review.urls")),
    path('manual_exception/',include("manual_exception.urls")),
    path('calloverexceptionreview/',include("calloverexceptionreview.urls")),
    path('CalloverforControl/',include("CalloverforControl.urls")),
    path('pendingcalloverforcontrol/',include("pendingcalloverforcontrol.urls")),
    path('calloverforcontrolspecial/',include("calloverforcontrolspecial.urls")),
    path('pendingcalloverforcontrolspecial/',include("pendingcalloverforcontrolspecial.urls")),
    path('userapp/', include('userapp.urls')),
    
    path('admin/', admin.site.urls),
    
    path('upload/', views.upload, name='upload-book'),
    
    # path('delete/<int:book_id>', views.delete_book),
    path('testing/',views.testing),
    path('book_delete/',views.book_Delete, name='book_delete'),
    path('search/',views.search,name='search'),
    path('', include('CheckComp.urls')),
    url(r'^accounts/', include('allauth.urls')),
    
    # path('acc_trans/<voucher_id>', views.acc_trans, name='acc_trans'),
    path('prof_trans/<Profile_ID>', views.Profile_Trans, name='prof_trans'),
    path('delete/<id>', views.delete_book, name='trans_id'),
    path('update/', views.update_trans, name='updated'),
    path('check_ocr/', views.OCR, name="OCR"),
    path('check_ocr2/', views.OCR2, name="OCR2"),
    
    path('observation/', views.Observation, name="Observation"),
    path('load/', views.load, name = 'load'),
    # path('')
    # path('pdf/', views.pdf_test, name ='pdf')
    # path('test/', views.test, name = 'test')
    # url(r'^pdf1', views.pdf1, name='pdf1'),
    # url(r'^accounts/', include('allauth.urls'))
    # path('call/', views.callover),
    # path('signup/'vie)
]




urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
