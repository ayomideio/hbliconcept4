from io import BytesIO


import requests
import time

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q



from iconcept4.models import *

from django.http import HttpResponseRedirect,HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd
from iconcept4.models import IC4_Callover
from iconcept4.queries import *
from django.db import connection
from django.urls import reverse
from iconcept4.services.ldap import get_LDAP_user
from userapp.models import Roless
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.utils

import socket
from datetime import datetime
today=datetime.date(datetime.now())
date_time=datetime.now()


from iconcept4.views import useractivity
from django.core.mail import send_mail,get_connection
from iconcept4.views import returnallbranch
from iconcept4.views import dictfetchall
# 172.27.4.4 80


branch_cd="0"

def index(request):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):

        b_c = ''
        username=request.session['userparam']
        pbranch=request.session['secondarybranch']
        today_date = '19-JUL-18'
        
        b_c=returnallbranch(request.session['secondarybranch'],request.session['username'])
        print(b_c)
        cursor = connection.cursor()
        result = cursor.execute('''
               SELECT "A1"."ID" "ID","A1"."CALLOVER_ID" "CALLOVER_ID","A1"."BRANCH_CODE" "BRANCH_CODE","A1"."OBSERVATION" "OBSERVATION","A1"."SEVERITY_LEVEL" "SEVERITY_LEVEL","A1"."EXCEPTION_STATUS" "EXCEPTION_STATUS","A1"."CALLOVER_LEVEL" "CALLOVER_LEVEL","A1"."OWNER_DETAIL" "OWNER_DETAIL","A1"."INPUTTER_EMAIL" "INPUTTER_EMAIL","A1"."EXCEPTION_DETAIL" "EXCEPTION_DETAIL","A1"."IMPLICATION" "IMPLICATION","A1"."ACTION" "ACTION","A1"."OTHER_RECEIVERS" "OTHER_RECEIVERS","A1"."ALERT_COMMENTS" "ALERT_COMMENTS","A1"."ACCEPTED_BY" "ACCEPTED_BY","A1"."ACCEPTED_DATE" "ACCEPTED_DATE","A1"."CHECKER_DATE_TIME" "CHECKER_DATE_TIME","A1"."IC4_SEVERITY_LEVEL_ID" "IC4_SEVERITY_LEVEL_ID","A1"."INPUTTER_NAME" "INPUTTER_NAME","A1"."ISSUE_PRIORITY" "ISSUE_PRIORITY","A1"."MATURITY_RATING" "MATURITY_RATING","A1"."OWNER_NAME" "OWNER_NAME","A1"."REVIEW" "REVIEW","A1"."TREE_ID" "TREE_ID","A1"."CALLOVER_OFFICER" "CALLOVER_OFFICER", TO_CHAR("A1"."CALLOVER_DATE", 'YYYY-MM-DD') "CALLOVER_DATE","A1"."CHECKER_ID" "CHECKER_ID","A1"."SUPERVISOR" "SUPERVISOR" FROM  (SELECT "A2"."ID" "ID","A2"."CALLOVER_ID" "CALLOVER_ID","A2"."BRANCH_CODE" "BRANCH_CODE","A2"."OBSERVATION" "OBSERVATION","A2"."SEVERITY_LEVEL" "SEVERITY_LEVEL","A2"."EXCEPTION_STATUS" "EXCEPTION_STATUS","A2"."CALLOVER_LEVEL" "CALLOVER_LEVEL","A2"."OWNER_DETAIL" "OWNER_DETAIL","A2"."INPUTTER_EMAIL" "INPUTTER_EMAIL","A2"."EXCEPTION_DETAIL" "EXCEPTION_DETAIL","A2"."IMPLICATION" "IMPLICATION","A2"."ACTION" "ACTION","A2"."OTHER_RECEIVERS" "OTHER_RECEIVERS","A2"."ALERT_COMMENTS" "ALERT_COMMENTS","A2"."ACCEPTED_BY" "ACCEPTED_BY","A2"."ACCEPTED_DATE" "ACCEPTED_DATE","A2"."CHECKER_DATE_TIME" "CHECKER_DATE_TIME","A2"."IC4_SEVERITY_LEVEL_ID" "IC4_SEVERITY_LEVEL_ID","A2"."INPUTTER_NAME" "INPUTTER_NAME","A2"."ISSUE_PRIORITY" "ISSUE_PRIORITY","A2"."MATURITY_RATING" "MATURITY_RATING","A2"."OWNER_NAME" "OWNER_NAME","A2"."REVIEW" "REVIEW","A2"."TREE_ID" "TREE_ID","A2"."CALLOVER_OFFICER" "CALLOVER_OFFICER","A2"."CALLOVER_DATE" "CALLOVER_DATE","A2"."CHECKER_ID" "CHECKER_ID","A2"."SUPERVISOR" "SUPERVISOR" FROM  (SELECT "A3"."ID" "ID","A3"."CALLOVER_ID" "CALLOVER_ID","A3"."BRANCH_CODE" "BRANCH_CODE","A3"."OBSERVATION" "OBSERVATION","A3"."SEVERITY_LEVEL" "SEVERITY_LEVEL","A3"."EXCEPTION_STATUS" "EXCEPTION_STATUS","A3"."CALLOVER_LEVEL" "CALLOVER_LEVEL","A3"."OWNER_DETAIL" "OWNER_DETAIL","A3"."INPUTTER_EMAIL" "INPUTTER_EMAIL","A3"."EXCEPTION_DETAIL" "EXCEPTION_DETAIL","A3"."IMPLICATION" "IMPLICATION","A3"."ACTION" "ACTION","A3"."OTHER_RECEIVERS" "OTHER_RECEIVERS","A3"."ALERT_COMMENTS" "ALERT_COMMENTS","A3"."ACCEPTED_BY" "ACCEPTED_BY","A3"."ACCEPTED_DATE" "ACCEPTED_DATE","A3"."CHECKER_DATE_TIME" "CHECKER_DATE_TIME","A3"."IC4_SEVERITY_LEVEL_ID" "IC4_SEVERITY_LEVEL_ID","A3"."INPUTTER_NAME" "INPUTTER_NAME","A3"."ISSUE_PRIORITY" "ISSUE_PRIORITY","A3"."MATURITY_RATING" "MATURITY_RATING","A3"."OWNER_NAME" "OWNER_NAME","A3"."REVIEW" "REVIEW","A3"."TREE_ID" "TREE_ID","A3"."CALLOVER_OFFICER" "CALLOVER_OFFICER","A3"."CALLOVER_DATE" "CALLOVER_DATE","A3"."CHECKER_ID" "CHECKER_ID","A3"."SUPERVISOR" "SUPERVISOR" FROM  (SELECT "A4"."ID" "ID","A4"."CALLOVER_ID" "CALLOVER_ID","A4"."BRANCH_CODE" "BRANCH_CODE","A4"."OBSERVATION" "OBSERVATION","A4"."SEVERITY_LEVEL" "SEVERITY_LEVEL","A4"."EXCEPTION_STATUS" "EXCEPTION_STATUS","A4"."CALLOVER_LEVEL" "CALLOVER_LEVEL","A4"."OWNER_DETAIL" "OWNER_DETAIL","A4"."INPUTTER_EMAIL" "INPUTTER_EMAIL","A4"."EXCEPTION_DETAIL" "EXCEPTION_DETAIL","A4"."IMPLICATION" "IMPLICATION","A4"."ACTION" "ACTION","A4"."OTHER_RECEIVERS" "OTHER_RECEIVERS","A4"."ALERT_COMMENTS" "ALERT_COMMENTS","A4"."ACCEPTED_BY" "ACCEPTED_BY","A4"."ACCEPTED_DATE" "ACCEPTED_DATE","A4"."CHECKER_DATE_TIME" "CHECKER_DATE_TIME","A4"."IC4_SEVERITY_LEVEL_ID" "IC4_SEVERITY_LEVEL_ID","A4"."INPUTTER_NAME" "INPUTTER_NAME","A4"."ISSUE_PRIORITY" "ISSUE_PRIORITY","A4"."MATURITY_RATING" "MATURITY_RATING","A4"."OWNER_NAME" "OWNER_NAME","A4"."REVIEW" "REVIEW","A4"."TREE_ID" "TREE_ID","A4"."CALLOVER_OFFICER" "CALLOVER_OFFICER","A4"."CALLOVER_DATE" "CALLOVER_DATE","A4"."CHECKER_ID" "CHECKER_ID","A4"."SUPERVISOR" "SUPERVISOR" FROM "U_IC4INDEP"."CALLOVER_EXCEPTION" "A4" WHERE
"A4"."EXCEPTION_STATUS"<>'CLOSE' AND ("A4"."OWNER_DETAIL"=%(username1)s OR "A4"."OTHER_RECEIVERS" IN 'ibukun.akinteye@adroitsolutionsltd.com,' OR "A4"."SUPERVISOR"=%(username1)s OR "A4"."INPUTTER_EMAIL"=%(username1)s OR "A4"."CALLOVER_OFFICER"=%(username1)s) ORDER BY "A4"."ID" DESC) "A3") "A2") "A1" 

                        ''',{'username1':request.session['username']})

        yList = dictfetchall(cursor)
    
    
        columns = [col[0] for col in cursor.description]
        print(yList)
        # profiles = IC4_Profile.objects.all()

        profiles = Profile.objects.all()
     
        return render(request, 'calloverExceptionGrid.html', {'results':yList, 'Profiles':profiles, 'test':branch_cd,'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
    else:
        return HttpResponseRedirect(reverse('login'))
    
def clickfromMail(request,calloverid):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):

        b_c = ''
        username=request.session['userparam']
        pbranch=request.session['secondarybranch']
        today_date = '19-JUL-18'
        query2 = '''SELECT BRANCH_CODE FROM USER_BRANCHES WHERE USER_ID='{0}'  '''.format(username)
        useractivity(request.session.session_key,"Callover Exception Review",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        request.session['username'],today_date,"Sucess","Click",request.session.session_key,"Callover Exception Review",
        """ {0} clicked on exception with callover id {1} from mail sent via iconcept4""".format(request.session['username'],calloverid),today,today_date)
        
        cursor2=connection.cursor()
        result2=cursor2.execute('''SELECT BRANCH_CODE FROM USER_BRANCHES WHERE USER_ID=%s  ''',(username))
        yList2=dictfetchall(cursor2)
        # print(yList2)
        for index in range(len(yList2)):
            for key in yList2[index]:
                b_c+=yList2[index][key]+","
                b=''
                # newb_c+=""" """
            
                # print(yList2[index][key])
                # print(b_c)
        b_c+=request.session['secondarybranch']
        print(b_c)
        cursor = connection.cursor()
        result = cursor.execute('''
               SELECT "A1"."ID" "ID","A1"."CALLOVER_ID" "CALLOVER_ID","A1"."BRANCH_CODE" "BRANCH_CODE",
               "A1"."OBSERVATION" "OBSERVATION","A1"."SEVERITY_LEVEL" "SEVERITY_LEVEL",
               "A1"."EXCEPTION_STATUS" "EXCEPTION_STATUS","A1"."CALLOVER_LEVEL" "CALLOVER_LEVEL",
               "A1"."OWNER_DETAIL" "OWNER_DETAIL","A1"."INPUTTER_EMAIL" "INPUTTER_EMAIL",
               "A1"."EXCEPTION_DETAIL" "EXCEPTION_DETAIL","A1"."IMPLICATION" "IMPLICATION",
               "A1"."ACTION" "ACTION","A1"."OTHER_RECEIVERS" "OTHER_RECEIVERS",
               "A1"."ALERT_COMMENTS" "ALERT_COMMENTS","A1"."ACCEPTED_BY" "ACCEPTED_BY",
               "A1"."ACCEPTED_DATE" "ACCEPTED_DATE","A1"."CHECKER_DATE_TIME" "CHECKER_DATE_TIME",
               "A1"."IC4_SEVERITY_LEVEL_ID" "IC4_SEVERITY_LEVEL_ID",
               "A1"."INPUTTER_NAME" "INPUTTER_NAME","A1"."ISSUE_PRIORITY" "ISSUE_PRIORITY",
               "A1"."MATURITY_RATING" "MATURITY_RATING","A1"."OWNER_NAME" "OWNER_NAME",
               "A1"."REVIEW" "REVIEW","A1"."TREE_ID" "TREE_ID","A1"."CALLOVER_OFFICER" "CALLOVER_OFFICER", 
               TO_CHAR("A1"."CALLOVER_DATE", 'YYYY-MM-DD') "CALLOVER_DATE","A1"."CHECKER_ID" "CHECKER_ID",
               "A1"."SUPERVISOR" "SUPERVISOR" FROM  (SELECT "A2"."ID" "ID","A2"."CALLOVER_ID" "CALLOVER_ID",
               "A2"."BRANCH_CODE" "BRANCH_CODE","A2"."OBSERVATION" "OBSERVATION","A2"."SEVERITY_LEVEL" "SEVERITY_LEVEL",
               "A2"."EXCEPTION_STATUS" "EXCEPTION_STATUS","A2"."CALLOVER_LEVEL" "CALLOVER_LEVEL",
               "A2"."OWNER_DETAIL" "OWNER_DETAIL","A2"."INPUTTER_EMAIL" "INPUTTER_EMAIL",
               "A2"."EXCEPTION_DETAIL" "EXCEPTION_DETAIL","A2"."IMPLICATION" "IMPLICATION",
               "A2"."ACTION" "ACTION","A2"."OTHER_RECEIVERS" "OTHER_RECEIVERS",
               "A2"."ALERT_COMMENTS" "ALERT_COMMENTS","A2"."ACCEPTED_BY" "ACCEPTED_BY",
               "A2"."ACCEPTED_DATE" "ACCEPTED_DATE","A2"."CHECKER_DATE_TIME" "CHECKER_DATE_TIME",
               "A2"."IC4_SEVERITY_LEVEL_ID" "IC4_SEVERITY_LEVEL_ID","A2"."INPUTTER_NAME" "INPUTTER_NAME",
               "A2"."ISSUE_PRIORITY" "ISSUE_PRIORITY","A2"."MATURITY_RATING" "MATURITY_RATING",
               "A2"."OWNER_NAME" "OWNER_NAME","A2"."REVIEW" "REVIEW","A2"."TREE_ID" "TREE_ID",
               "A2"."CALLOVER_OFFICER" "CALLOVER_OFFICER","A2"."CALLOVER_DATE" "CALLOVER_DATE",
               "A2"."CHECKER_ID" "CHECKER_ID","A2"."SUPERVISOR" "SUPERVISOR" FROM  
               (SELECT "A3"."ID" "ID","A3"."CALLOVER_ID" "CALLOVER_ID","A3"."BRANCH_CODE" "BRANCH_CODE",
               "A3"."OBSERVATION" "OBSERVATION","A3"."SEVERITY_LEVEL" "SEVERITY_LEVEL",
               "A3"."EXCEPTION_STATUS" "EXCEPTION_STATUS","A3"."CALLOVER_LEVEL" "CALLOVER_LEVEL",
               "A3"."OWNER_DETAIL" "OWNER_DETAIL","A3"."INPUTTER_EMAIL" "INPUTTER_EMAIL",
               "A3"."EXCEPTION_DETAIL" "EXCEPTION_DETAIL","A3"."IMPLICATION" "IMPLICATION",
               "A3"."ACTION" "ACTION","A3"."OTHER_RECEIVERS" "OTHER_RECEIVERS","A3"."ALERT_COMMENTS" "ALERT_COMMENTS",
               "A3"."ACCEPTED_BY" "ACCEPTED_BY","A3"."ACCEPTED_DATE" "ACCEPTED_DATE",
               "A3"."CHECKER_DATE_TIME" "CHECKER_DATE_TIME","A3"."IC4_SEVERITY_LEVEL_ID" "IC4_SEVERITY_LEVEL_ID",
               "A3"."INPUTTER_NAME" "INPUTTER_NAME","A3"."ISSUE_PRIORITY" "ISSUE_PRIORITY","A3"."MATURITY_RATING" "MATURITY_RATING","A3"."OWNER_NAME" "OWNER_NAME","A3"."REVIEW" "REVIEW","A3"."TREE_ID" "TREE_ID","A3"."CALLOVER_OFFICER" "CALLOVER_OFFICER","A3"."CALLOVER_DATE" "CALLOVER_DATE","A3"."CHECKER_ID" "CHECKER_ID","A3"."SUPERVISOR" "SUPERVISOR" FROM  (SELECT "A4"."ID" "ID","A4"."CALLOVER_ID" "CALLOVER_ID",
               "A4"."BRANCH_CODE" "BRANCH_CODE","A4"."OBSERVATION" "OBSERVATION","A4"."SEVERITY_LEVEL" "SEVERITY_LEVEL","A4"."EXCEPTION_STATUS" "EXCEPTION_STATUS","A4"."CALLOVER_LEVEL" "CALLOVER_LEVEL","A4"."OWNER_DETAIL" "OWNER_DETAIL","A4"."INPUTTER_EMAIL" "INPUTTER_EMAIL","A4"."EXCEPTION_DETAIL" "EXCEPTION_DETAIL","A4"."IMPLICATION" "IMPLICATION","A4"."ACTION" "ACTION","A4"."OTHER_RECEIVERS" "OTHER_RECEIVERS","A4"."ALERT_COMMENTS" "ALERT_COMMENTS","A4"."ACCEPTED_BY" "ACCEPTED_BY","A4"."ACCEPTED_DATE" "ACCEPTED_DATE",
               "A4"."CHECKER_DATE_TIME" "CHECKER_DATE_TIME","A4"."IC4_SEVERITY_LEVEL_ID" "IC4_SEVERITY_LEVEL_ID","A4"."INPUTTER_NAME" "INPUTTER_NAME","A4"."ISSUE_PRIORITY" "ISSUE_PRIORITY","A4"."MATURITY_RATING" "MATURITY_RATING","A4"."OWNER_NAME" "OWNER_NAME","A4"."REVIEW" "REVIEW",
               "A4"."TREE_ID" "TREE_ID","A4"."CALLOVER_OFFICER" "CALLOVER_OFFICER","A4"."CALLOVER_DATE" "CALLOVER_DATE",
               "A4"."CHECKER_ID" "CHECKER_ID","A4"."SUPERVISOR" "SUPERVISOR" 
                    FROM "U_IC4INDEP"."CALLOVER_EXCEPTION" "A4" 
                    WHERE "A4"."EXCEPTION_STATUS"<>'CLOSE'  
                    AND "A4"."CALLOVER_ID" = %s
                    ORDER BY "A4"."ID" DESC) "A3") "A2") "A1" ''',(calloverid))

        yList = dictfetchall(cursor)
    
    
        columns = [col[0] for col in cursor.description]
        print(yList)
        # profiles = IC4_Profile.objects.all()

        profiles = Profile.objects.all()

                
        return render(request, 'calloverExceptionGrid.html', {'results':yList, 'Profiles':profiles, 'test':branch_cd,'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
    else:
        return HttpResponseRedirect(reverse('login'))
    


# @staff_member_required
def Exception_Detail(request, callover_id):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):

        request.session['arraytest']=""
        
        cursor = connection.cursor()
        useractivity(request.session.session_key,"Callover Exception Review",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        request.session['username'],today_date,"Sucess","Click",request.session.session_key,"Callover Exception Review",
        """ {0} clicked on exception with callover id {1} """.format(request.session['username'],callover_id),today,today_date)
        
        cursor.execute('''   SELECT "A1"."ID" "ID","A1"."CALLOVER_ID" "CALLOVER_ID","A1"."BRANCH_CODE" "BRANCH_CODE","A1"."OBSERVATION" "OBSERVATION","A1"."SEVERITY_LEVEL" "SEVERITY_LEVEL","A1"."EXCEPTION_STATUS" "EXCEPTION_STATUS","A1"."CALLOVER_LEVEL" "CALLOVER_LEVEL","A1"."OWNER_DETAIL" "OWNER_DETAIL","A1"."INPUTTER_EMAIL" "INPUTTER_EMAIL","A1"."EXCEPTION_DETAIL" "EXCEPTION_DETAIL","A1"."IMPLICATION" "IMPLICATION","A1"."ACTION" "ACTION","A1"."OTHER_RECEIVERS" "OTHER_RECEIVERS","A1"."ALERT_COMMENTS" "ALERT_COMMENTS","A1"."ACCEPTED_BY" "ACCEPTED_BY","A1"."ACCEPTED_DATE" "ACCEPTED_DATE","A1"."CHECKER_DATE_TIME" "CHECKER_DATE_TIME","A1"."IC4_SEVERITY_LEVEL_ID" "IC4_SEVERITY_LEVEL_ID","A1"."INPUTTER_NAME" "INPUTTER_NAME","A1"."ISSUE_PRIORITY" "ISSUE_PRIORITY","A1"."MATURITY_RATING" "MATURITY_RATING","A1"."OWNER_NAME" "OWNER_NAME","A1"."REVIEW" "REVIEW","A1"."TREE_ID" "TREE_ID","A1"."CALLOVER_OFFICER" "CALLOVER_OFFICER", TO_CHAR("A1"."CALLOVER_DATE", 'YYYY-MM-DD') "CALLOVER_DATE","A1"."CHECKER_ID" "CHECKER_ID","A1"."SUPERVISOR" "SUPERVISOR" FROM  (SELECT "A2"."ID" "ID","A2"."CALLOVER_ID" "CALLOVER_ID","A2"."BRANCH_CODE" "BRANCH_CODE","A2"."OBSERVATION" "OBSERVATION","A2"."SEVERITY_LEVEL" "SEVERITY_LEVEL","A2"."EXCEPTION_STATUS" "EXCEPTION_STATUS","A2"."CALLOVER_LEVEL" "CALLOVER_LEVEL","A2"."OWNER_DETAIL" "OWNER_DETAIL","A2"."INPUTTER_EMAIL" "INPUTTER_EMAIL","A2"."EXCEPTION_DETAIL" "EXCEPTION_DETAIL","A2"."IMPLICATION" "IMPLICATION","A2"."ACTION" "ACTION","A2"."OTHER_RECEIVERS" "OTHER_RECEIVERS","A2"."ALERT_COMMENTS" "ALERT_COMMENTS","A2"."ACCEPTED_BY" "ACCEPTED_BY","A2"."ACCEPTED_DATE" "ACCEPTED_DATE","A2"."CHECKER_DATE_TIME" "CHECKER_DATE_TIME","A2"."IC4_SEVERITY_LEVEL_ID" "IC4_SEVERITY_LEVEL_ID","A2"."INPUTTER_NAME" "INPUTTER_NAME","A2"."ISSUE_PRIORITY" "ISSUE_PRIORITY","A2"."MATURITY_RATING" "MATURITY_RATING","A2"."OWNER_NAME" "OWNER_NAME","A2"."REVIEW" "REVIEW","A2"."TREE_ID" "TREE_ID","A2"."CALLOVER_OFFICER" "CALLOVER_OFFICER","A2"."CALLOVER_DATE" "CALLOVER_DATE","A2"."CHECKER_ID" "CHECKER_ID","A2"."SUPERVISOR" "SUPERVISOR" FROM  (SELECT "A3"."ID" "ID","A3"."CALLOVER_ID" "CALLOVER_ID","A3"."BRANCH_CODE" "BRANCH_CODE","A3"."OBSERVATION" "OBSERVATION","A3"."SEVERITY_LEVEL" "SEVERITY_LEVEL","A3"."EXCEPTION_STATUS" "EXCEPTION_STATUS","A3"."CALLOVER_LEVEL" "CALLOVER_LEVEL","A3"."OWNER_DETAIL" "OWNER_DETAIL","A3"."INPUTTER_EMAIL" "INPUTTER_EMAIL","A3"."EXCEPTION_DETAIL" "EXCEPTION_DETAIL","A3"."IMPLICATION" "IMPLICATION","A3"."ACTION" "ACTION","A3"."OTHER_RECEIVERS" "OTHER_RECEIVERS","A3"."ALERT_COMMENTS" "ALERT_COMMENTS","A3"."ACCEPTED_BY" "ACCEPTED_BY","A3"."ACCEPTED_DATE" "ACCEPTED_DATE","A3"."CHECKER_DATE_TIME" "CHECKER_DATE_TIME","A3"."IC4_SEVERITY_LEVEL_ID" "IC4_SEVERITY_LEVEL_ID","A3"."INPUTTER_NAME" "INPUTTER_NAME","A3"."ISSUE_PRIORITY" "ISSUE_PRIORITY","A3"."MATURITY_RATING" "MATURITY_RATING","A3"."OWNER_NAME" "OWNER_NAME","A3"."REVIEW" "REVIEW","A3"."TREE_ID" "TREE_ID","A3"."CALLOVER_OFFICER" "CALLOVER_OFFICER","A3"."CALLOVER_DATE" "CALLOVER_DATE","A3"."CHECKER_ID" "CHECKER_ID","A3"."SUPERVISOR" "SUPERVISOR" FROM  (SELECT "A4"."ID" "ID","A4"."CALLOVER_ID" "CALLOVER_ID","A4"."BRANCH_CODE" "BRANCH_CODE","A4"."OBSERVATION" "OBSERVATION","A4"."SEVERITY_LEVEL" "SEVERITY_LEVEL","A4"."EXCEPTION_STATUS" "EXCEPTION_STATUS","A4"."CALLOVER_LEVEL" "CALLOVER_LEVEL","A4"."OWNER_DETAIL" "OWNER_DETAIL","A4"."INPUTTER_EMAIL" "INPUTTER_EMAIL","A4"."EXCEPTION_DETAIL" "EXCEPTION_DETAIL","A4"."IMPLICATION" "IMPLICATION","A4"."ACTION" "ACTION","A4"."OTHER_RECEIVERS" "OTHER_RECEIVERS","A4"."ALERT_COMMENTS" "ALERT_COMMENTS","A4"."ACCEPTED_BY" "ACCEPTED_BY","A4"."ACCEPTED_DATE" "ACCEPTED_DATE","A4"."CHECKER_DATE_TIME" "CHECKER_DATE_TIME","A4"."IC4_SEVERITY_LEVEL_ID" "IC4_SEVERITY_LEVEL_ID","A4"."INPUTTER_NAME" "INPUTTER_NAME","A4"."ISSUE_PRIORITY" "ISSUE_PRIORITY","A4"."MATURITY_RATING" "MATURITY_RATING","A4"."OWNER_NAME" "OWNER_NAME","A4"."REVIEW" "REVIEW","A4"."TREE_ID" "TREE_ID","A4"."CALLOVER_OFFICER" "CALLOVER_OFFICER","A4"."CALLOVER_DATE" "CALLOVER_DATE","A4"."CHECKER_ID" "CHECKER_ID","A4"."SUPERVISOR" "SUPERVISOR" FROM "U_IC4INDEP"."CALLOVER_EXCEPTION" "A4" WHERE
                            "A4"."EXCEPTION_STATUS"<>'CLOSE' AND A4.CALLOVER_ID= %(calloverid)s  ORDER BY "A4"."ID" DESC) "A3") "A2") "A1"
                            ''',{'calloverid':callover_id})
        
        request.session['selectedbranch'] =callover_id
        isOwner=''
        owner=IC4_CALLOVER_EXCEPTION.objects.get(CallOver_ID=callover_id)
        if (owner.Owner_Detail == request.session['userparam']):
            isOwner='YES'
    


        
        
        yList = dictfetchall(cursor)
        
        
        
    
        module='Callover for Teller'
    
    
    
        return render(request, 'CalloverException.html', {'results': yList,'isOwner':isOwner,'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
    
    else:

        return HttpResponseRedirect(reverse('login'))
        

           



def Accept(request):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):

        sdsignal=request.POST['sendSignal']
    

        calloverId=request.POST['calloverId']
        branchCode=request.POST['branchCode']
        observation=request.POST['observation']
        severity=request.POST['severity']
        exceptionStatus=request.POST['exceptionStatus']
        calloverLevel=request.POST['calloverLevel']
        owners=request.POST['owners']
        inputterEmail=request.POST['inputterEmail']
        observationdetails=request.POST['observationdetails']
        implication=request.POST['implication']
        action=request.POST['action']
        otherReceivers=request.POST['otherReceivers']
        comments=request.POST['comments']
        calloverOfficer=request.POST['calloverOfficer']
        calloverDate=request.POST['calloverDate']
        checkerIdentity=request.POST['checkerIdentity']
        supervisor=request.POST['supervisor']


        print(sdsignal)
        if (sdsignal== 'send'):
            exceptionfilter=IC4_CALLOVER_EXCEPTION.objects.get(CallOver_ID=calloverId)
            # atadebiyi@unionbankng.com [2019-08-15 17:58:06]: REGULARIZED. RE OCCURRENCE NOW GUIDED"
            today=datetime.now()
            stringDate=today.strftime("%m%d%Y,%H:%M:%S")
            temp_alertcomments=exceptionfilter.Alert_Comments
            temp_alertcomments+='\n'
            temp_alertcomments+=request.session['userparam']
            temp_alertcomments+=' ['+ stringDate + ']: ' +comments
            exceptionfilter.Alert_Comments=temp_alertcomments
            exceptionfilter.Other_Receivers=otherReceivers
            exceptionfilter.Exception_Status='RESPONSE'
            subject = 'Callover Exception Response '
            call=exceptionfilter.CallOver_ID
            a="""\
                    <html lang="en"><head><style>body{{margin:0;padding:0;overflow-x:auto!important;overflow-y:hidden!important}}.mail-detail-content{{box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;font-size:13px;font-weight:400;font-feature-settings:"liga" 0;width:100%;position:relative;padding:0}}.ios.smartphone .mail-detail-content{{-webkit-overflow-scrolling:touch;overflow-x:auto}}.smartphone .mail-detail-content{{font-size:15px}}.mail-detail-content>div>[class$="-content"]{{padding:0}}.mail-detail-content.plain-text{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;white-space:pre-wrap}}.mail-detail-content.plain-text blockquote{{white-space:normal}}.mail-detail-content.fixed-width-font,.mail-detail-content.fixed-width-font.plain-text,.mail-detail-content.fixed-width-font blockquote,.mail-detail-content.fixed-width-font.plain-text blockquote,.mail-detail-content.fixed-width-font blockquote p,.mail-detail-content.fixed-width-font.plain-text blockquote p{{font-family:monospace;-webkit-font-feature-settings:normal;font-feature-settings:normal}}.mail-detail-content.simple-mail{{max-width:700px}}.mail-detail-content.simple-mail.big-screen{{max-width:100%}}.mail-detail-content.simple-mail img{{max-width:100%;height:auto!important}}.mail-detail-content img[src=""]{{background-color:rgba(0,0,0,.1);background-image:repeating-linear-gradient(45deg,transparent,transparent 20px,rgba(255,255,255,.5) 20px,rgba(255,255,255,.5) 40px)}}.mail-detail-content p{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;margin:0 0 1em}}.mail-detail-content h1{{font-size:28px}}.mail-detail-content h2{{font-size:21px}}.mail-detail-content h3{{font-size:16.38px}}.mail-detail-content h4{{font-size:14px}}.mail-detail-content h5{{font-size:11.62px}}.mail-detail-content h6{{font-size:9.38px}}.mail-detail-content a{{word-break:break-word;text-decoration:none;color:inherit}}.mail-detail-content a:hover{{color:inherit}}.mail-detail-content a[href]{{color:#3c61aa;text-decoration:underline}}.mail-detail-content th{{padding:8px;text-align:center}}.mail-detail-content th[align=left]{{text-align:left}}.mail-detail-content .calendar-detail .label{{display:block;text-shadow:none;font-weight:400;background-color:transparent}}.mail-detail-content img.emoji-softbank{{margin:0 2px}}.mail-detail-content pre{{word-break:keep-all;word-break:initial;white-space:pre-wrap;background-color:transparent;border:0 none;border-radius:0}}.mail-detail-content table{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;font-size:13px;font-weight:400;font-feature-settings:"liga" 0;line-height:normal;border-collapse:collapse}}.mail-detail-content ul,.mail-detail-content ol{{padding:0;padding-left:16px;margin:1em 0 1em 24px}}.mail-detail-content ul{{list-style-type:disc}}.mail-detail-content ul ul{{list-style-type:circle}}.mail-detail-content ul ul ul{{list-style-type:square}}.mail-detail-content li{{line-height:normal;margin-bottom:.5em}}.mail-detail-content blockquote{{color:#555;font-size:13px;border-left:2px solid #ddd;padding:0 0 0 16px;margin:16px 0}}.mail-detail-content blockquote p{{font-size:13px}}.mail-detail-content blockquote blockquote{{border-color:#283f73;margin:8px 0}}.mail-detail-content.colorQuoted blockquote blockquote{{color:#283f73!important;border-left:2px solid #283f73}}.mail-detail-content.colorQuoted blockquote blockquote a[href]:not(.deep-link){{color:#283f73}}.mail-detail-content.colorQuoted blockquote blockquote a[href]:not(.deep-link):hover{{color:#1b2a4d}}.mail-detail-content.colorQuoted blockquote blockquote blockquote{{color:#dd0880!important;border-left:2px solid #dd0880}}.mail-detail-content.colorQuoted blockquote blockquote blockquote a[href]:not(.deep-link){{color:#dd0880}}.mail-detail-content.colorQuoted blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#ac0663}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote{{color:#8f09c7!important;border-left:2px solid #8f09c7}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote a[href]:not(.deep-link){{color:#8f09c7}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#6c0796}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote{{color:#767676!important;border-left:2px solid #767676}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote a[href]:not(.deep-link){{color:#767676}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#5d5d5d}}.mail-detail-content.disable-links a[href]{{color:#aaa!important;text-decoration:line-through!important;cursor:default!important;pointer-events:none!important}}.mail-detail-content .blockquote-toggle{{color:#767676;font-size:13px;padding-left:56px;margin:16px 0;min-height:16px;word-break:break-word}}.mail-detail-content .blockquote-toggle button.bqt{{color:#696969;background-color:#eee;padding:1px 10px;display:inline-block;font-size:14px;line-height:16px;cursor:pointer;outline:0;position:absolute;left:0;border:0}}.mail-detail-content .blockquote-toggle button.bqt:hover,.mail-detail-content .blockquote-toggle button.bqt:focus{{color:#fff;background-color:#3c61aa;text-decoration:none}}.mail-detail-content .max-size-warning{{color:#767676;padding:16px 16px 0;border-top:1px solid #ddd}}.mail-detail-content a.deep-link{{color:#fff;background-color:#3c61aa;text-decoration:none;font-size:90%;font-weight:700;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif!important;padding:.1em 8px;border-radius:3px}}.mail-detail-content a.deep-link:hover,.mail-detail-content a.deep-link:focus,.mail-detail-content a.deep-link:active{{color:#fff;background-color:#2f4b84}}@media print{{.mail-detail-content .collapsed-blockquote{{display:block!important}}.mail-detail-content .blockquote-toggle{{display:none!important}}.mail-detail-content>div[id*=ox-]>h1,.mail-detail-content>div[id*=ox-]>h2,.mail-detail-content>div[id*=ox-]>h3,.mail-detail-content>div[id*=ox-]>h4,.mail-detail-content>div[id*=ox-]>h5{{margin-top:0}}</style>
                    <style>.mail-detail-content .alertHeader {{ text-align: center; line-height: 30px; font-size: 16px; color: rgb(51, 51, 51); font-weight: bold; width: 100%; }} .mail-detail-content .ControlAlert {{ background-color: rgb(173, 216, 230); }} .mail-detail-content .internalControlAlert {{ background-color: rgb(156, 207, 0); }} .mail-detail-content .auditImplication {{ background-color: rgb(0, 112, 192); }} .mail-detail-content .action {{ background-color: rgb(49, 154, 99); }} .mail-detail-content .additional_info {{ background-color: rgb(153, 109, 144); }} .mail-detail-content .alertLabel {{ line-height: 20px; font-size: 12px; color: rgb(51, 51, 51); font-weight: bold; width: 150px; }} .mail-detail-content .alertValue {{ line-height: 20px; font-size: 12px; color: black; width: 100%; }} .mail-detail-content .cell {{ border: 1px solid black; width: 30%; padding: 5px; text-align: left; }} </style>
        
                    </head>
                    <body class="mail-detail-content noI18n colorQuoted">
        
        
        
                    

                        <table cellspacing="0" cellpadding="0" border="0" width="70%" style="margin:0 auto; margin-top:2rem">
                            <tbody><tr>
                                <td colspan="2" class="alertHeader internalControlAlert">CALLOVER
                                EXCEPTION REVIEW CONFIRM
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre style="margin-bottom: 1rem;">{6}</pre>
                                                        
                            </td></tr>
                            <tr>
                                <td colspan="2" class="alertHeader auditImplication">IMPLICATION
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre class="alertValue" style="margin-bottom: 1rem;">{8}</pre>
                                </td><td>
                            </td></tr>
                            <tr>
                                <td colspan="2" class="alertHeader action">ACTION
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre class="alertValue" style="margin-bottom: 1rem;">{7}</pre>
                                </td><td>
                        </td></tr>
                        
                        <tr>
                                <td colspan="2" class="alertHeader ControlAlert">TRANSACTION DETAILS 
                        </td></tr>
                        <tr>
                            <td class="cell">TRANSACTION REFERENCE</td>
                            <td class="cell">{1}</td>
                        </tr>
                        <tr>
                            <td class="cell">TRANSACTION DATE</td>
                            <td style="border: 1px solid black; width: 60%; padding: 5px;">{2}</td>
                        </tr>

                        <tr>
                            <td class="cell">BRANCH CODE</td>
                            <td class="cell">'{0}'</td>
                        </tr>
                        <tr>
                            <td class="cell">INPUTTER</td>
                            <td class="cell"><a href="mailto:{3}" class="mailto-link" target="_blank">{3}</a></td>
                        </tr>
                        <tr>
                            <td class="cell">SEVERITY</td>
                            <td class="cell">{4}</td>
                        </tr>
                        <td class="cell">COMMENTS</td>
                            <td class="cell">{5}</td>
                        </tbody></table>

                        </body></html> """.format(calloverId,exceptionfilter.Maturity_Rating,
                        exceptionfilter.Issue_Priority,exceptionfilter.Inputter_Email,exceptionfilter.Severity_Level,
                        exceptionfilter.Alert_Comments,exceptionfilter.Observation,exceptionfilter.Action,exceptionfilter.Implication )  
            sender_email = "adegokeadeleke.ayo@gmail.com"
            receiver_email = [otherReceivers,calloverOfficer,supervisor,inputterEmail,owners]

            password = "alvvcakmxqbfgvfa"
            message = MIMEMultipart("alternative")
            message["Subject"] = "Callover Exception Response -"+exceptionfilter.CallOver_ID
            message["From"] = request.session["username"]
            message["To"] =','.join(receiver_email)   
            today=datetime.date(datetime.now())
            useractivity(request.session.session_key,"Callover Exception Review",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        request.session['username'],today_date,"Sucess","Click",request.session.session_key,"Callover Exception Review",
        """ {0} responded to exception with callover id {1} """.format(request.session['username'],exceptionfilter.CallOver_ID),today,today)
        
        
        
            # socks.setdefaultproxy(socks.SOCKS5, 'proxy.', 8080)
            # socks.wrapmodule(smtplib)
            part2 = MIMEText(a, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            # message.attach(part1)
            message.attach(part2)
            myid = email.utils.make_msgid()
            # exceptionfilter.CallOver_ID=myid
            message.add_header("In-Reply-To",exceptionfilter.CallOver_ID)
            message.add_header("References", exceptionfilter.CallOver_ID)
            # Create secure connection with server and send email
            context = ssl.create_default_context()
        
            cursor=connection.cursor()
            results=cursor.execute("""SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailAddress' """)
            # username=cursor.fetchone()
            for result in results:
                username = result[0]
            results=cursor.execute("""SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailServer' """)
            # username=cursor.fetchone()
            for result in results:
                smtpserver = result[0]
            results=cursor.execute("""SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailPort' """)
            # username=cursor.fetchone()
            for result in results:
                smtpport = result[0]
            results=cursor.execute("""SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailUserPassword' """)
            # username=cursor.fetchone()
            for result in results:
                password = result[0]
            to = receiver_email
            # 'ayodeji.ajimisinmi@wemabank.com'
            print(">>>>>>>>>>",username)
            usename=""
            # usename+=str(username)
            exceptionfilter.save()
            gmail_user = request.session["username"]
            gmail_pwd = 'Iconcept4nbas'
            smtpserver = smtplib.SMTP("""{0}""".format(smtpserver),"""{0}""".format(smtpport))
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            
            smtpserver.sendmail(gmail_user, to,message.as_string())
        
            smtpserver.close()
        
            print('SUCCESS')

    
        
            
            
            
            

            
        else:
            exceptionfilter=IC4_CALLOVER_EXCEPTION.objects.get(CallOver_ID=calloverId)
            # atadebiyi@unionbankng.com [2019-08-15 17:58:06]: REGULARIZED. RE OCCURRENCE NOW GUIDED"
            today=datetime.now()
            stringDate=today.strftime("%m%d%Y,%H:%M:%S")
            temp_alertcomments=exceptionfilter.Alert_Comments
            temp_alertcomments+='\n'
            temp_alertcomments+=request.session['userparam']
            temp_alertcomments+=' ['+ stringDate + ']: ' +comments
            exceptionfilter.Alert_Comments=temp_alertcomments
            exceptionfilter.Other_Receivers=otherReceivers
            exceptionfilter.Exception_Status='CLOSE'
            a="""\
                    <html lang="en"><head><style>body{{margin:0;padding:0;overflow-x:auto!important;overflow-y:hidden!important}}.mail-detail-content{{box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;font-size:13px;font-weight:400;font-feature-settings:"liga" 0;width:100%;position:relative;padding:0}}.ios.smartphone .mail-detail-content{{-webkit-overflow-scrolling:touch;overflow-x:auto}}.smartphone .mail-detail-content{{font-size:15px}}.mail-detail-content>div>[class$="-content"]{{padding:0}}.mail-detail-content.plain-text{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;white-space:pre-wrap}}.mail-detail-content.plain-text blockquote{{white-space:normal}}.mail-detail-content.fixed-width-font,.mail-detail-content.fixed-width-font.plain-text,.mail-detail-content.fixed-width-font blockquote,.mail-detail-content.fixed-width-font.plain-text blockquote,.mail-detail-content.fixed-width-font blockquote p,.mail-detail-content.fixed-width-font.plain-text blockquote p{{font-family:monospace;-webkit-font-feature-settings:normal;font-feature-settings:normal}}.mail-detail-content.simple-mail{{max-width:700px}}.mail-detail-content.simple-mail.big-screen{{max-width:100%}}.mail-detail-content.simple-mail img{{max-width:100%;height:auto!important}}.mail-detail-content img[src=""]{{background-color:rgba(0,0,0,.1);background-image:repeating-linear-gradient(45deg,transparent,transparent 20px,rgba(255,255,255,.5) 20px,rgba(255,255,255,.5) 40px)}}.mail-detail-content p{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;margin:0 0 1em}}.mail-detail-content h1{{font-size:28px}}.mail-detail-content h2{{font-size:21px}}.mail-detail-content h3{{font-size:16.38px}}.mail-detail-content h4{{font-size:14px}}.mail-detail-content h5{{font-size:11.62px}}.mail-detail-content h6{{font-size:9.38px}}.mail-detail-content a{{word-break:break-word;text-decoration:none;color:inherit}}.mail-detail-content a:hover{{color:inherit}}.mail-detail-content a[href]{{color:#3c61aa;text-decoration:underline}}.mail-detail-content th{{padding:8px;text-align:center}}.mail-detail-content th[align=left]{{text-align:left}}.mail-detail-content .calendar-detail .label{{display:block;text-shadow:none;font-weight:400;background-color:transparent}}.mail-detail-content img.emoji-softbank{{margin:0 2px}}.mail-detail-content pre{{word-break:keep-all;word-break:initial;white-space:pre-wrap;background-color:transparent;border:0 none;border-radius:0}}.mail-detail-content table{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;font-size:13px;font-weight:400;font-feature-settings:"liga" 0;line-height:normal;border-collapse:collapse}}.mail-detail-content ul,.mail-detail-content ol{{padding:0;padding-left:16px;margin:1em 0 1em 24px}}.mail-detail-content ul{{list-style-type:disc}}.mail-detail-content ul ul{{list-style-type:circle}}.mail-detail-content ul ul ul{{list-style-type:square}}.mail-detail-content li{{line-height:normal;margin-bottom:.5em}}.mail-detail-content blockquote{{color:#555;font-size:13px;border-left:2px solid #ddd;padding:0 0 0 16px;margin:16px 0}}.mail-detail-content blockquote p{{font-size:13px}}.mail-detail-content blockquote blockquote{{border-color:#283f73;margin:8px 0}}.mail-detail-content.colorQuoted blockquote blockquote{{color:#283f73!important;border-left:2px solid #283f73}}.mail-detail-content.colorQuoted blockquote blockquote a[href]:not(.deep-link){{color:#283f73}}.mail-detail-content.colorQuoted blockquote blockquote a[href]:not(.deep-link):hover{{color:#1b2a4d}}.mail-detail-content.colorQuoted blockquote blockquote blockquote{{color:#dd0880!important;border-left:2px solid #dd0880}}.mail-detail-content.colorQuoted blockquote blockquote blockquote a[href]:not(.deep-link){{color:#dd0880}}.mail-detail-content.colorQuoted blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#ac0663}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote{{color:#8f09c7!important;border-left:2px solid #8f09c7}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote a[href]:not(.deep-link){{color:#8f09c7}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#6c0796}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote{{color:#767676!important;border-left:2px solid #767676}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote a[href]:not(.deep-link){{color:#767676}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#5d5d5d}}.mail-detail-content.disable-links a[href]{{color:#aaa!important;text-decoration:line-through!important;cursor:default!important;pointer-events:none!important}}.mail-detail-content .blockquote-toggle{{color:#767676;font-size:13px;padding-left:56px;margin:16px 0;min-height:16px;word-break:break-word}}.mail-detail-content .blockquote-toggle button.bqt{{color:#696969;background-color:#eee;padding:1px 10px;display:inline-block;font-size:14px;line-height:16px;cursor:pointer;outline:0;position:absolute;left:0;border:0}}.mail-detail-content .blockquote-toggle button.bqt:hover,.mail-detail-content .blockquote-toggle button.bqt:focus{{color:#fff;background-color:#3c61aa;text-decoration:none}}.mail-detail-content .max-size-warning{{color:#767676;padding:16px 16px 0;border-top:1px solid #ddd}}.mail-detail-content a.deep-link{{color:#fff;background-color:#3c61aa;text-decoration:none;font-size:90%;font-weight:700;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif!important;padding:.1em 8px;border-radius:3px}}.mail-detail-content a.deep-link:hover,.mail-detail-content a.deep-link:focus,.mail-detail-content a.deep-link:active{{color:#fff;background-color:#2f4b84}}@media print{{.mail-detail-content .collapsed-blockquote{{display:block!important}}.mail-detail-content .blockquote-toggle{{display:none!important}}.mail-detail-content>div[id*=ox-]>h1,.mail-detail-content>div[id*=ox-]>h2,.mail-detail-content>div[id*=ox-]>h3,.mail-detail-content>div[id*=ox-]>h4,.mail-detail-content>div[id*=ox-]>h5{{margin-top:0}}</style>
                    <style>.mail-detail-content .alertHeader {{ text-align: center; line-height: 30px; font-size: 16px; color: rgb(51, 51, 51); font-weight: bold; width: 100%; }} .mail-detail-content .ControlAlert {{ background-color: rgb(173, 216, 230); }} .mail-detail-content .internalControlAlert {{ background-color: rgb(156, 207, 0); }} .mail-detail-content .auditImplication {{ background-color: rgb(0, 112, 192); }} .mail-detail-content .action {{ background-color: rgb(49, 154, 99); }} .mail-detail-content .additional_info {{ background-color: rgb(153, 109, 144); }} .mail-detail-content .alertLabel {{ line-height: 20px; font-size: 12px; color: rgb(51, 51, 51); font-weight: bold; width: 150px; }} .mail-detail-content .alertValue {{ line-height: 20px; font-size: 12px; color: black; width: 100%; }} .mail-detail-content .cell {{ border: 1px solid black; width: 30%; padding: 5px; text-align: left; }} </style>
        
                    </head>
                    <body class="mail-detail-content noI18n colorQuoted">
        
        
        
                    

                        <table cellspacing="0" cellpadding="0" border="0" width="70%" style="margin:0 auto; margin-top:2rem">
                            <tbody><tr>
                                <td colspan="2" class="alertHeader internalControlAlert">CALLOVER
                                EXCEPTION REVIEW CONFIRM
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre style="margin-bottom: 1rem;">Huge multiple transfer from the same person the same day</pre>
                                                        
                            </td></tr>
                            <tr>
                                <td colspan="2" class="alertHeader auditImplication">IMPLICATION
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre class="alertValue" style="margin-bottom: 1rem;">Risk of fraud and possibility of wrongful disclosure, litigation</pre>
                                </td><td>
                            </td></tr>
                            <tr>
                                <td colspan="2" class="alertHeader action">ACTION
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre class="alertValue" style="margin-bottom: 1rem;">Request customer to complete the signature, inline with mandate</pre>
                                </td><td>
                        </td></tr>
                        
                        <tr>
                                <td colspan="2" class="alertHeader ControlAlert">TRANSACTION DETAILS 
                        </td></tr>
                        <tr>
                            <td class="cell">TRANSACTION REFERENCE</td>
                            <td class="cell">{1}</td>
                        </tr>
                        <tr>
                            <td class="cell">TRANSACTION DATE</td>
                            <td style="border: 1px solid black; width: 60%; padding: 5px;">{2}</td>
                        </tr>

                        <tr>
                            <td class="cell">BRANCH CODE</td>
                            <td class="cell">'{0}'</td>
                        </tr>
                        <tr>
                            <td class="cell">INPUTTER</td>
                            <td class="cell"><a href="mailto:{3}" class="mailto-link" target="_blank">{3}</a></td>
                        </tr>
                        <tr>
                            <td class="cell">SEVERITY</td>
                            <td class="cell">{4}</td>
                        </tr>
                        <tr>
                            <td class="cell">COMMENTS</td>
                            <td class="cell">{5}</td>
                        </tr>
                        </tbody></table>

                        </body></html> """.format(calloverId,exceptionfilter.Maturity_Rating,exceptionfilter.Issue_Priority,exceptionfilter.Inputter_Email,exceptionfilter.Severity_Level,exceptionfilter.Alert_Comments )  
            sender_email = "adegokeadeleke.ayo@gmail.com"
            receiver_email = [otherReceivers,calloverOfficer,supervisor,inputterEmail,owners]

            password = "alvvcakmxqbfgvfa"
            message = MIMEMultipart("alternative")
            message["Subject"] = "Callover Exception Response -"+exceptionfilter.CallOver_ID
            message["From"] = request.session["username"]
            message["To"] =','.join(receiver_email)   

            today=datetime.date(datetime.now())
            useractivity(request.session.session_key,"Callover Exception Review",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        request.session['username'],today_date,"Sucess","Click",request.session.session_key,"Callover Exception Review",
        """ {0} closed to exception with callover id {1} """.format(request.session['username'],exceptionfilter.CallOver_ID),today,today)
        
        
            # socks.setdefaultproxy(socks.SOCKS5, 'proxy.', 8080)
            # socks.wrapmodule(smtplib)
            part2 = MIMEText(a, "html")

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            # message.attach(part1)
            message.attach(part2)
            myid = email.utils.make_msgid()
            # exceptionfilter.CallOver_ID=myid
            message.add_header("In-Reply-To",exceptionfilter.CallOver_ID)
            message.add_header("References", exceptionfilter.CallOver_ID)
            # Create secure connection with server and send email
            context = ssl.create_default_context()
        
            cursor=connection.cursor()
            results=cursor.execute("""SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailAddress' """)
            # username=cursor.fetchone()
            for result in results:
                username = result[0]
            results=cursor.execute("""SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailServer' """)
            # username=cursor.fetchone()
            for result in results:
                smtpserver = result[0]
            results=cursor.execute("""SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailPort' """)
            # username=cursor.fetchone()
            for result in results:
                smtpport = result[0]
            results=cursor.execute("""SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailUserPassword' """)
            # username=cursor.fetchone()
            for result in results:
                password = result[0]
            to = receiver_email
            # 'ayodeji.ajimisinmi@wemabank.com'
            print(">>>>>>>>>>",username)
            usename=""
            # usename+=str(username)
            exceptionfilter.save()
            gmail_user = request.session["username"]
            gmail_pwd = 'Iconcept4nbas'
            smtpserver = smtplib.SMTP("""{0}""".format(smtpserver),"""{0}""".format(smtpport))
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            
            smtpserver.sendmail(gmail_user, to,message.as_string())
        
            smtpserver.close()
        
            print('SUCCESS')


            


        
        return HttpResponseRedirect(reverse('calloverexceptionreviewindex'))
    

    else:
        return HttpResponseRedirect(reverse('login'))

      

   
               

