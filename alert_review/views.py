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
from django.core.mail import send_mail,get_connection
from django.core.files.storage import FileSystemStorage
from email.mime.application import MIMEApplication
from os.path import basename
from iconcept4.views import dictfetchall    ,returnallbranch, useractivity
# 172.27.4.4 80


branch_cd="0"


def index(request,id):
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
        SELECT * FROM (select /*+ FIRST_ROWS(20) */ a.* FROM (SELECT * FROM (SELECT ID, ALERT_ID, BRANCH_CODE, EXCEPTION_NAME, SEVERITY_LEVEL, OWNER, 
                        OWNER_DETAIL, NEXT_OWNER, NEXT_OWNER_DETAIL, RESPONDENT, RESPONDENT_DETAIL, OTHER_RECEIVER_EMAILS, DATE_CREATED, REVIEW_DATE, TO_CHAR(INVESTIGATION)INVESTIGATION, 
                        NEXT_RESPONDENT, NEXT_RESPONDENT_DETAIL, NEXT_NOTIFIER, NEXT_NOTIFIER_DETAIL, TO_CHAR(ALERT_COMMENTS) ALERT_COMMENTS, INVESTIGATE_ID, ACCEPTED_BY, ACCEPTED_DATE, 
                        IC4_ACCOUNT_OFFICER, IC4_INPUTTER, IC4_AUTHORISER, IC4_VERIFIER, IC4_SPECIAL, IC4_TRANS_ID, IC4_TRANS_REF_ID, IC4_TRANS_TYPE, IC4_TRANS_CODE, 
                        IC4_SORT_CODE, IC4_ACCOUNT_NO, IC4_ACCOUNT_NAME, IC4_CUSTOMER_NO, IC4_POST_DATE, IC4_BOOKING_DATE, IC4_VALUE_DATE, IC4_TRANS_CCY, IC4_TRANS_AMOUNT, 
                        IC4_LOCAL_CCY, IC4_LOCAL_AMOUNT, IC4_FOREIGN_AMOUNT, IC4_RATES, IC4_CHEQUE_NO, IC4_NARRATIVE, IC4_NOTE_1, IC4_NOTE_2, IC4_NOTE_3, IC4_NOTE_4, 
                        IC4_NOTE_5, IC4_NOTE_6, IC4_TIME_STAMP, IC4_SEVERITY_LEVEL_ID 
                        FROM U_IC4INDEP.ALERT_DETAILS  
                        WHERE (LOWER(OWNER_DETAIL) IN %(username1)s OR LOWER(NEXT_OWNER_DETAIL) IN %(username1)s 
                        OR LOWER(RESPONDENT_DETAIL) IN %(username1)s OR LOWER(NEXT_RESPONDENT_DETAIL) IN %(username1)s 
                        OR LOWER(NEXT_NOTIFIER_DETAIL) IN %(username1)s) 
                        AND ALERT_ID = %(alertid)s 
                        AND ACCEPTED_BY IS NULL
                        ORDER BY ID DESC) a ) a ) b
                        
UNION

SELECT * FROM (select /*+ FIRST_ROWS(20) */ a.* FROM (SELECT * FROM (SELECT ID, ALERT_ID, BRANCH_CODE, EXCEPTION_NAME, SEVERITY_LEVEL, OWNER, 
                        OWNER_DETAIL, NEXT_OWNER, NEXT_OWNER_DETAIL, RESPONDENT, RESPONDENT_DETAIL, OTHER_RECEIVER_EMAILS, DATE_CREATED, REVIEW_DATE, TO_CHAR(INVESTIGATION) INVESTIGATION, 
                        NEXT_RESPONDENT, NEXT_RESPONDENT_DETAIL, NEXT_NOTIFIER, NEXT_NOTIFIER_DETAIL, TO_CHAR(ALERT_COMMENTS) ALERT_COMMENTS, INVESTIGATE_ID, ACCEPTED_BY, ACCEPTED_DATE, 
                        IC4_ACCOUNT_OFFICER, IC4_INPUTTER, IC4_AUTHORISER, IC4_VERIFIER, IC4_SPECIAL, IC4_TRANS_ID, IC4_TRANS_REF_ID, IC4_TRANS_TYPE, IC4_TRANS_CODE, 
                        IC4_SORT_CODE, IC4_ACCOUNT_NO, IC4_ACCOUNT_NAME, IC4_CUSTOMER_NO, IC4_POST_DATE, IC4_BOOKING_DATE, IC4_VALUE_DATE, IC4_TRANS_CCY, IC4_TRANS_AMOUNT, 
                        IC4_LOCAL_CCY, IC4_LOCAL_AMOUNT, IC4_FOREIGN_AMOUNT, IC4_RATES, IC4_CHEQUE_NO, IC4_NARRATIVE, IC4_NOTE_1, IC4_NOTE_2, IC4_NOTE_3, IC4_NOTE_4, 
                        IC4_NOTE_5, IC4_NOTE_6, IC4_TIME_STAMP, IC4_SEVERITY_LEVEL_ID 
                        FROM U_IC4INDEP.ALERT_DETAILS  
                        WHERE (LOWER(OWNER_DETAIL) IN %(username2)s OR LOWER(NEXT_OWNER_DETAIL) IN %(username2)s 
                        OR LOWER(RESPONDENT_DETAIL) IN %(username2)s OR LOWER(NEXT_RESPONDENT_DETAIL) IN %(username2)s 
                        OR LOWER(NEXT_NOTIFIER_DETAIL) IN %(username2)s) 
                        AND ALERT_ID = %(alertid)s 
                        AND ACCEPTED_BY IS NULL
                        ORDER BY ID DESC) a ) a ) b
 
                                    
                                                ''',{'username1':request.session['username']+';','username2':request.session['username'],'alertid':id})

        yList = dictfetchall(cursor)
    
    
        columns = [col[0] for col in cursor.description]
        # print(yList)
        # profiles = IC4_Profile.objects.all()

        profiles = Profile.objects.all()
        
        return render(request, 'InvestigationManagerGrid.html', {'results':yList, 'Profiles':profiles, 'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
    else:
        return HttpResponseRedirect(reverse('login'))

def indexall(request):
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
                                  SELECT * FROM (select /*+ FIRST_ROWS(20) */ a.* FROM (SELECT * FROM (SELECT ID, ALERT_ID, BRANCH_CODE, EXCEPTION_NAME, SEVERITY_LEVEL, OWNER, 
                        OWNER_DETAIL, NEXT_OWNER, NEXT_OWNER_DETAIL, RESPONDENT, RESPONDENT_DETAIL, OTHER_RECEIVER_EMAILS, DATE_CREATED, REVIEW_DATE, TO_CHAR(INVESTIGATION)INVESTIGATION, 
                        NEXT_RESPONDENT, NEXT_RESPONDENT_DETAIL, NEXT_NOTIFIER, NEXT_NOTIFIER_DETAIL, TO_CHAR(ALERT_COMMENTS) ALERT_COMMENTS, INVESTIGATE_ID, ACCEPTED_BY, ACCEPTED_DATE, 
                        IC4_ACCOUNT_OFFICER, IC4_INPUTTER, IC4_AUTHORISER, IC4_VERIFIER, IC4_SPECIAL, IC4_TRANS_ID, IC4_TRANS_REF_ID, IC4_TRANS_TYPE, IC4_TRANS_CODE, 
                        IC4_SORT_CODE, IC4_ACCOUNT_NO, IC4_ACCOUNT_NAME, IC4_CUSTOMER_NO, IC4_POST_DATE, IC4_BOOKING_DATE, IC4_VALUE_DATE, IC4_TRANS_CCY, IC4_TRANS_AMOUNT, 
                        IC4_LOCAL_CCY, IC4_LOCAL_AMOUNT, IC4_FOREIGN_AMOUNT, IC4_RATES, IC4_CHEQUE_NO, IC4_NARRATIVE, IC4_NOTE_1, IC4_NOTE_2, IC4_NOTE_3, IC4_NOTE_4, 
                        IC4_NOTE_5, IC4_NOTE_6, IC4_TIME_STAMP, IC4_SEVERITY_LEVEL_ID 
                        FROM U_IC4INDEP.ALERT_DETAILS  
                        WHERE (LOWER(OWNER_DETAIL) IN %(username1)s OR LOWER(NEXT_OWNER_DETAIL) IN %(username1)s 
                        OR LOWER(RESPONDENT_DETAIL) IN %(username1)s OR LOWER(NEXT_RESPONDENT_DETAIL) IN %(username1)s 
                        OR LOWER(NEXT_NOTIFIER_DETAIL) IN %(username1)s) 
                        
                        AND ACCEPTED_BY IS NULL
                        ORDER BY ID DESC) a ) a ) b
                        
UNION

SELECT * FROM (select /*+ FIRST_ROWS(20) */ a.* FROM (SELECT * FROM (SELECT ID, ALERT_ID, BRANCH_CODE, EXCEPTION_NAME, SEVERITY_LEVEL, OWNER, 
                        OWNER_DETAIL, NEXT_OWNER, NEXT_OWNER_DETAIL, RESPONDENT, RESPONDENT_DETAIL, OTHER_RECEIVER_EMAILS, DATE_CREATED, REVIEW_DATE, TO_CHAR(INVESTIGATION) INVESTIGATION, 
                        NEXT_RESPONDENT, NEXT_RESPONDENT_DETAIL, NEXT_NOTIFIER, NEXT_NOTIFIER_DETAIL, TO_CHAR(ALERT_COMMENTS) ALERT_COMMENTS, INVESTIGATE_ID, ACCEPTED_BY, ACCEPTED_DATE, 
                        IC4_ACCOUNT_OFFICER, IC4_INPUTTER, IC4_AUTHORISER, IC4_VERIFIER, IC4_SPECIAL, IC4_TRANS_ID, IC4_TRANS_REF_ID, IC4_TRANS_TYPE, IC4_TRANS_CODE, 
                        IC4_SORT_CODE, IC4_ACCOUNT_NO, IC4_ACCOUNT_NAME, IC4_CUSTOMER_NO, IC4_POST_DATE, IC4_BOOKING_DATE, IC4_VALUE_DATE, IC4_TRANS_CCY, IC4_TRANS_AMOUNT, 
                        IC4_LOCAL_CCY, IC4_LOCAL_AMOUNT, IC4_FOREIGN_AMOUNT, IC4_RATES, IC4_CHEQUE_NO, IC4_NARRATIVE, IC4_NOTE_1, IC4_NOTE_2, IC4_NOTE_3, IC4_NOTE_4, 
                        IC4_NOTE_5, IC4_NOTE_6, IC4_TIME_STAMP, IC4_SEVERITY_LEVEL_ID 
                        FROM U_IC4INDEP.ALERT_DETAILS  
                        WHERE (LOWER(OWNER_DETAIL) IN %(username2)s OR LOWER(NEXT_OWNER_DETAIL) IN %(username2)s 
                        OR LOWER(RESPONDENT_DETAIL) IN %(username2)s OR LOWER(NEXT_RESPONDENT_DETAIL) IN %(username2)s 
                        OR LOWER(NEXT_NOTIFIER_DETAIL) IN %(username2)s) 
                        
                        AND ACCEPTED_BY IS NULL
                        ORDER BY ID DESC) a ) a ) b
 
                                                ''',{'username1':request.session['username']+';','username2':request.session['username']})

        yList = dictfetchall(cursor)
    
    
        columns = [col[0] for col in cursor.description]
        # print(yList)
        # profiles = IC4_Profile.objects.all()

        profiles = Profile.objects.all()

                  
        return render(request, 'InvestigationManagerGrid.html', {'results':yList, 'Profiles':profiles, 'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
    else:
        return HttpResponseRedirect(reverse('login'))


def indexoffollow(request):
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
                                   SELECT * FROM (select /*+ FIRST_ROWS(20) */ a.* FROM (SELECT * FROM (SELECT ID, ALERT_ID, EXCEPTION_NAME, BRANCH_CODE, SEVERITY_LEVEL, OWNER, 
                            OWNER_DETAIL, NEXT_OWNER, NEXT_OWNER_DETAIL, RESPONDENT, RESPONDENT_DETAIL, OTHER_RECIVERS, OTHER_RECIVERS_UPDATE, MATURITY_RATING, 
                            ISSUE_PRIORITY, RISK_INDICATOR, REVIEW, ALERT_COMMENT, EXCEPTION_DETAIL, ACCEPTED_BY, ACCEPT_DATE 
                            FROM U_IC4INDEP.ALERT_JOURNAL 
                            WHERE (LOWER(OWNER_DETAIL) LIKE '%{0}%' OR LOWER(NEXT_OWNER_DETAIL) LIKE '%{0}%' 
                            OR LOWER(RESPONDENT_DETAIL) LIKE '%{0}%' OR LOWER(OTHER_RECIVERS) LIKE '%{0}%' ) 
                            
                            AND NVL(ACCEPTED_BY,'null')='null' 
                            ORDER BY ID DESC) a ) a ) b
                                                '''.format(request.session['username']), None)

        yList = dictfetchall(cursor)
    
    
        columns = [col[0] for col in cursor.description]
        # print(yList)
        # profiles = IC4_Profile.objects.all()

        profiles = Profile.objects.all()

            
        return render(request, 'followupgrid.html', {'results':yList, 'Profiles':profiles, 'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
    else:
        return HttpResponseRedirect(reverse('login'))

def indexoffollowall(request):
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
                                   SELECT * FROM (select /*+ FIRST_ROWS(20) */ a.* FROM (SELECT * FROM (SELECT ID, ALERT_ID, EXCEPTION_NAME, BRANCH_CODE, SEVERITY_LEVEL, OWNER, 
                            OWNER_DETAIL, NEXT_OWNER, NEXT_OWNER_DETAIL, RESPONDENT, RESPONDENT_DETAIL, OTHER_RECIVERS, OTHER_RECIVERS_UPDATE, MATURITY_RATING, 
                            ISSUE_PRIORITY, RISK_INDICATOR, REVIEW, ALERT_COMMENT, EXCEPTION_DETAIL, ACCEPTED_BY, ACCEPT_DATE 
                            FROM U_IC4INDEP.ALERT_JOURNAL 
                            WHERE (LOWER(OWNER_DETAIL) LIKE '%{0}%' OR LOWER(NEXT_OWNER_DETAIL) LIKE '%{0}%' 
                            OR LOWER(RESPONDENT_DETAIL) LIKE '%{0}%' OR LOWER(OTHER_RECIVERS) LIKE '%{0}%' ) 
                
                            AND NVL(ACCEPTED_BY,'null')='null' 
                            AND EXCEPTION_DETAIL IS NOT NULL
                            AND ROWNUM < 11 
                            ORDER BY ID DESC) a ) a ) b
                                                '''.format(request.session['username']), None)

        yList = dictfetchall(cursor)
    
    
        columns = [col[0] for col in cursor.description]
        # print(yList)
        # profiles = IC4_Profile.objects.all()

        profiles = Profile.objects.all()

        return render(request, 'followupgrid.html', {'results':yList, 'Profiles':profiles, 'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
    else:
        return HttpResponseRedirect(reverse('login'))


def Followup_Detail(request,callover_id):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):

        request.session['arraytest']=""
        
        cursor = connection.cursor()
        useractivity(request.session.session_key,"Follow Up",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        request.session['username'],today_date,"Sucess","Click",request.session.session_key,"Follow Up",
        """ {0} clicked on follow up with alert id {1} """.format(request.session['username'],callover_id),today,today_date)
        

        cursor.execute('''           SELECT * FROM (select /*+ FIRST_ROWS(20) */ a.* FROM (SELECT * FROM (SELECT ID, ALERT_ID, EXCEPTION_NAME, BRANCH_CODE, SEVERITY_LEVEL, OWNER, 
                            OWNER_DETAIL, NEXT_OWNER, NEXT_OWNER_DETAIL, RESPONDENT, RESPONDENT_DETAIL, OTHER_RECIVERS, OTHER_RECIVERS_UPDATE, MATURITY_RATING, 
                            ISSUE_PRIORITY, RISK_INDICATOR, REVIEW, ALERT_COMMENT, EXCEPTION_DETAIL, ACCEPTED_BY, ACCEPT_DATE 
                            FROM U_IC4INDEP.ALERT_JOURNAL 
                            WHERE LOWER(OWNER_DETAIL) IN %(username)s  OR LOWER(NEXT_OWNER_DETAIL) IN %(username)s 
                            OR LOWER(RESPONDENT_DETAIL) IN %(username)s  OR LOWER(OTHER_RECIVERS) IN %(username)s 
                           
                            AND NVL(ACCEPTED_BY,'null')='null' 
                            ORDER BY ID DESC) a ) a ) b
UNION ALL

 SELECT * FROM (select /*+ FIRST_ROWS(20) */ a.* FROM (SELECT * FROM (SELECT ID, ALERT_ID, EXCEPTION_NAME, BRANCH_CODE, SEVERITY_LEVEL, OWNER, 
                            OWNER_DETAIL, NEXT_OWNER, NEXT_OWNER_DETAIL, RESPONDENT, RESPONDENT_DETAIL, OTHER_RECIVERS, OTHER_RECIVERS_UPDATE, MATURITY_RATING, 
                            ISSUE_PRIORITY, RISK_INDICATOR, REVIEW, ALERT_COMMENT, EXCEPTION_DETAIL, ACCEPTED_BY, ACCEPT_DATE 
                            FROM U_IC4INDEP.ALERT_JOURNAL 
                            WHERE LOWER(OWNER_DETAIL) IN %(username2)s OR LOWER(NEXT_OWNER_DETAIL) IN %(username2)s 
                            OR LOWER(RESPONDENT_DETAIL) IN %(username2)s OR LOWER(OTHER_RECIVERS) IN %(username2)s 
                            
                            AND NVL(ACCEPTED_BY,'null')='null' 
                            ORDER BY ID DESC) a ) a ) b''',{'username':request.session['username']+';','username2':request.session['username']})
        # callover_id="CEZIAKONWA202101070700000010CHDP210070027"
        request.session['selectedbranch'] =callover_id
        isOwner='YES'
   
            
    


        
        
        yList =dictfetchall(cursor)
        # print(yList)
        cursor=connection.cursor()
        results=cursor.execute("""SELECT EXCEPTION_DETAIL FROM ALERT_JOURNAL WHERE ALERT_ID= '{0}' """.format(callover_id))
        # username=cursor.fetchone()
        for result in results:
            FORMAL = str(result[0])
        
        FORMAL.replace('''<style type="text/css">
.alertHeader {
	text-align: center;
	line-height: 30px;
	font-familly: Verdana;
	font-size: 16px;
	color: #333333;
	font-weight: bold;
	width: 100%;
}

.internalControlAlert {
	background-color: #9CCF00;
}

.auditImplication {
	background-color: #0070C0;
}

.action {
	background-color: #319A63;
}

.additional_info {
	background-color: #996d90;
}

.alertLabel {
	line-height: 20px;
	font-familly: Verdana;
	font-size: 12px;
	color: #333333;
	font-weight: bold;
	width: 150px;
}

.alertValue {
	line-height: 20px;
	font-familly: Verdana;
	font-size: 12px;
	color: black;
	width: 100%;
}
</style>''','')
        
        
        a="""\
        
                            {0}
                        

                              """.format(FORMAL)  
        FORMAL_P = MIMEText(a, "html") 
        
        
        module='Callover for Teller'
    
    
    
        return render(request, 'followup.html', {'htmb':FORMAL_P,'results': yList,'isOwner':isOwner,'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
    
    else:

        return HttpResponseRedirect(reverse('login'))
   


def clickfromMail(request,calloverid):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):

        b_c = ''
        username=request.session['userparam']
        pbranch=request.session['secondarybranch']
        today_date = '19-JUL-18'
        
        useractivity(request.session.session_key,"Alert Review",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        request.session['username'],today_date,"Sucess","Click",request.session.session_key,"Alert Review",
        """ {0} clicked on Alert Review with alert id {1} """.format(request.session['username'],calloverid),today,today_date)
        
        b_c=returnallbranch(request.session['secondarybranch'],request.session['username'])
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
def Exception_Detail(request,callover_id):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):

        request.session['arraytest']=""
        
        cursor = connection.cursor()
        useractivity(request.session.session_key,"Alert Review",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        request.session['username'],today_date,"Sucess","Click",request.session.session_key,"Alert Review",
        """ {0} clicked on Alert Review with alert id {1} """.format(request.session['username'],callover_id),today,today_date)
        

        cursor.execute('''             SELECT * FROM (select /*+ FIRST_ROWS(250) */ a.* FROM (SELECT * FROM (SELECT ID, ALERT_ID, BRANCH_CODE, EXCEPTION_NAME, SEVERITY_LEVEL, OWNER, 
                    OWNER_DETAIL, NEXT_OWNER, NEXT_OWNER_DETAIL, RESPONDENT, RESPONDENT_DETAIL, OTHER_RECEIVER_EMAILS, DATE_CREATED, REVIEW_DATE, INVESTIGATION, 
                    NEXT_RESPONDENT, NEXT_RESPONDENT_DETAIL, NEXT_NOTIFIER, NEXT_NOTIFIER_DETAIL, ALERT_COMMENTS, INVESTIGATE_ID, ACCEPTED_BY, ACCEPTED_DATE, 
                    IC4_ACCOUNT_OFFICER, IC4_INPUTTER, IC4_AUTHORISER, IC4_VERIFIER, IC4_SPECIAL, IC4_TRANS_ID, IC4_TRANS_REF_ID, IC4_TRANS_TYPE, IC4_TRANS_CODE, 
                    IC4_SORT_CODE, IC4_ACCOUNT_NO, IC4_ACCOUNT_NAME, IC4_CUSTOMER_NO, IC4_POST_DATE, IC4_BOOKING_DATE, IC4_VALUE_DATE, IC4_TRANS_CCY, IC4_TRANS_AMOUNT, 
                    IC4_LOCAL_CCY, IC4_LOCAL_AMOUNT, IC4_FOREIGN_AMOUNT, IC4_RATES, IC4_CHEQUE_NO, IC4_NARRATIVE, IC4_NOTE_1, IC4_NOTE_2, IC4_NOTE_3, IC4_NOTE_4, 
                    IC4_NOTE_5, IC4_NOTE_6, IC4_TIME_STAMP, IC4_SEVERITY_LEVEL_ID 
                    FROM U_IC4INDEP.ALERT_DETAILS  
                    WHERE ID=%(callover_id)s
                    ORDER BY ID DESC) a ) a ) b ''',{'callover_id':callover_id})
        # callover_id="CEZIAKONWA202101070700000010CHDP210070027"
        request.session['selectedbranch'] =''+callover_id
        isOwner='YES'
   
            
    


        
        
        yList =dictfetchall(cursor)
        # print(yList)
        
        
        
    
        module='Callover for Teller'
    
    
    
        return render(request, 'investigationmanager.html', {'results': yList,'isOwner':isOwner,'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
    
    else:

        return HttpResponseRedirect(reverse('login'))
        


def AcceptFollow(request):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):

        sdsignal=request.POST['sendSignal']
        today=datetime.now()
        stringDate=today.strftime("%m%d%Y,%H:%M:%S")
        comments=''
        Id=request.POST['id']
        alertid=request.POST['alertid']
        Investigation=''
        prev_comments=request.POST['prevcomments']
        cursor=connection.cursor()
        results=cursor.execute("""SELECT EXCEPTION_DETAIL FROM ALERT_JOURNAL WHERE ALERT_ID= %s """,(alertid))
        # username=cursor.fetchone()
        for result in results:
            FORMAL = str(result[0])
        
        FORMAL.replace('''<style type="text/css">
.alertHeader {
	text-align: center;
	line-height: 30px;
	font-familly: Verdana;
	font-size: 16px;
	color: #333333;
	font-weight: bold;
	width: 100%;
}

.internalControlAlert {
	background-color: #9CCF00;
}

.auditImplication {
	background-color: #0070C0;
}

.action {
	background-color: #319A63;
}

.additional_info {
	background-color: #996d90;
}

.alertLabel {
	line-height: 20px;
	font-familly: Verdana;
	font-size: 12px;
	color: #333333;
	font-weight: bold;
	width: 150px;
}

.alertValue {
	line-height: 20px;
	font-familly: Verdana;
	font-size: 12px;
	color: black;
	width: 100%;
}
</style>''','')
        comments+=prev_comments
        comments+='\n'+ request.session['userparam']
        comments+=' ['+ stringDate + ']: ' + request.POST['comments']
        a="""\
                                             <html lang="en"><head><style>body{{margin:0;padding:0;overflow-x:auto!important;overflow-y:hidden!important}}.mail-detail-content{{box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;font-size:13px;font-weight:400;font-feature-settings:"liga" 0;width:100%;position:relative;padding:0}}.ios.smartphone .mail-detail-content{{-webkit-overflow-scrolling:touch;overflow-x:auto}}.smartphone .mail-detail-content{{font-size:15px}}.mail-detail-content>div>[class$="-content"]{{padding:0}}.mail-detail-content.plain-text{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;white-space:pre-wrap}}.mail-detail-content.plain-text blockquote{{white-space:normal}}.mail-detail-content.fixed-width-font,.mail-detail-content.fixed-width-font.plain-text,.mail-detail-content.fixed-width-font blockquote,.mail-detail-content.fixed-width-font.plain-text blockquote,.mail-detail-content.fixed-width-font blockquote p,.mail-detail-content.fixed-width-font.plain-text blockquote p{{font-family:monospace;-webkit-font-feature-settings:normal;font-feature-settings:normal}}.mail-detail-content.simple-mail{{max-width:700px}}.mail-detail-content.simple-mail.big-screen{{max-width:100%}}.mail-detail-content.simple-mail img{{max-width:100%;height:auto!important}}.mail-detail-content img[src=""]{{background-color:rgba(0,0,0,.1);background-image:repeating-linear-gradient(45deg,transparent,transparent 20px,rgba(255,255,255,.5) 20px,rgba(255,255,255,.5) 40px)}}.mail-detail-content p{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;margin:0 0 1em}}.mail-detail-content h1{{font-size:28px}}.mail-detail-content h2{{font-size:21px}}.mail-detail-content h3{{font-size:16.38px}}.mail-detail-content h4{{font-size:14px}}.mail-detail-content h5{{font-size:11.62px}}.mail-detail-content h6{{font-size:9.38px}}.mail-detail-content a{{word-break:break-word;text-decoration:none;color:inherit}}.mail-detail-content a:hover{{color:inherit}}.mail-detail-content a[href]{{color:#3c61aa;text-decoration:underline}}.mail-detail-content th{{padding:8px;text-align:center}}.mail-detail-content th[align=left]{{text-align:left}}.mail-detail-content .calendar-detail .label{{display:block;text-shadow:none;font-weight:400;background-color:transparent}}.mail-detail-content img.emoji-softbank{{margin:0 2px}}.mail-detail-content pre{{word-break:keep-all;word-break:initial;white-space:pre-wrap;background-color:transparent;border:0 none;border-radius:0}}.mail-detail-content table{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;font-size:13px;font-weight:400;font-feature-settings:"liga" 0;line-height:normal;border-collapse:collapse}}.mail-detail-content ul,.mail-detail-content ol{{padding:0;padding-left:16px;margin:1em 0 1em 24px}}.mail-detail-content ul{{list-style-type:disc}}.mail-detail-content ul ul{{list-style-type:circle}}.mail-detail-content ul ul ul{{list-style-type:square}}.mail-detail-content li{{line-height:normal;margin-bottom:.5em}}.mail-detail-content blockquote{{color:#555;font-size:13px;border-left:2px solid #ddd;padding:0 0 0 16px;margin:16px 0}}.mail-detail-content blockquote p{{font-size:13px}}.mail-detail-content blockquote blockquote{{border-color:#283f73;margin:8px 0}}.mail-detail-content.colorQuoted blockquote blockquote{{color:#283f73!important;border-left:2px solid #283f73}}.mail-detail-content.colorQuoted blockquote blockquote a[href]:not(.deep-link){{color:#283f73}}.mail-detail-content.colorQuoted blockquote blockquote a[href]:not(.deep-link):hover{{color:#1b2a4d}}.mail-detail-content.colorQuoted blockquote blockquote blockquote{{color:#dd0880!important;border-left:2px solid #dd0880}}.mail-detail-content.colorQuoted blockquote blockquote blockquote a[href]:not(.deep-link){{color:#dd0880}}.mail-detail-content.colorQuoted blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#ac0663}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote{{color:#8f09c7!important;border-left:2px solid #8f09c7}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote a[href]:not(.deep-link){{color:#8f09c7}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#6c0796}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote{{color:#767676!important;border-left:2px solid #767676}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote a[href]:not(.deep-link){{color:#767676}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#5d5d5d}}.mail-detail-content.disable-links a[href]{{color:#aaa!important;text-decoration:line-through!important;cursor:default!important;pointer-events:none!important}}.mail-detail-content .blockquote-toggle{{color:#767676;font-size:13px;padding-left:56px;margin:16px 0;min-height:16px;word-break:break-word}}.mail-detail-content .blockquote-toggle button.bqt{{color:#696969;background-color:#eee;padding:1px 10px;display:inline-block;font-size:14px;line-height:16px;cursor:pointer;outline:0;position:absolute;left:0;border:0}}.mail-detail-content .blockquote-toggle button.bqt:hover,.mail-detail-content .blockquote-toggle button.bqt:focus{{color:#fff;background-color:#3c61aa;text-decoration:none}}.mail-detail-content .max-size-warning{{color:#767676;padding:16px 16px 0;border-top:1px solid #ddd}}.mail-detail-content a.deep-link{{color:#fff;background-color:#3c61aa;text-decoration:none;font-size:90%;font-weight:700;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif!important;padding:.1em 8px;border-radius:3px}}.mail-detail-content a.deep-link:hover,.mail-detail-content a.deep-link:focus,.mail-detail-content a.deep-link:active{{color:#fff;background-color:#2f4b84}}@media print{{.mail-detail-content .collapsed-blockquote{{display:block!important}}.mail-detail-content .blockquote-toggle{{display:none!important}}.mail-detail-content>div[id*=ox-]>h1,.mail-detail-content>div[id*=ox-]>h2,.mail-detail-content>div[id*=ox-]>h3,.mail-detail-content>div[id*=ox-]>h4,.mail-detail-content>div[id*=ox-]>h5{{margin-top:0}}</style>
                    <style>.mail-detail-content .alertHeader {{ text-align: center; line-height: 30px; font-size: 16px; color: rgb(51, 51, 51); font-weight: bold; width: 100%; }} .mail-detail-content .ControlAlert {{ background-color: rgb(173, 216, 230); }} .mail-detail-content .internalControlAlert {{ background-color: rgb(156, 207, 0); }} .mail-detail-content .auditImplication {{ background-color: rgb(0, 112, 192); }} .mail-detail-content .action {{ background-color: rgb(49, 154, 99); }} .mail-detail-content .additional_info {{ background-color: rgb(153, 109, 144); }} .mail-detail-content .alertLabel {{ line-height: 20px; font-size: 12px; color: rgb(51, 51, 51); font-weight: bold; width: 150px; }} .mail-detail-content .alertValue {{ line-height: 20px; font-size: 12px; color: black; width: 100%; }} .mail-detail-content .cell {{ border: 1px solid black; width: 30%; padding: 5px; text-align: left; }} </style>
        
                    </head>
                    <body class="mail-detail-content noI18n colorQuoted">
        
        
        
                        

                        <table cellspacing="0" cellpadding="0" border="0" width="70%" style="margin:0 auto; margin-top:2rem">
                            <tbody>
                                     
                            
                            <tr>
                                <td colspan="2" class="alertHeader internalControlAlert">Follow Up
                            </td></tr>
                          
                        
               
                           <tr>
                            <td class="cell">ALERT ID</td>
                            <td class="cell">{2}</td>
                        </tr>

                          <tr>
                            <td class="cell">BRANCH CODE</td>
                            <td class="cell">{3}</td>
                        </tr>
                      
                        <tr>
                            <td class="cell">COMMENTS</td>
                            <td style="border: 1px solid black; width: 60%; padding: 5px;">{1}</td>
                        </tr>

                             <tr>
                            <td class="cell">PREVIOUS COMMENTS</td>
                            <td style="border: 1px solid black; width: 60%; padding: 5px;">{5}</td>
                        </tr>

                       
                        </tbody></table>
                        <br><br/>
                        {4}
                        </body></html>        """.format(Investigation,request.POST['comments'],alertid,request.POST.get('branchCode'),FORMAL,request.POST.get('prevcomments') )  
        part2 = MIMEText(a, "html")                           
        sender_email = "adegokeadeleke.ayo@gmail.com"
        if(request.POST.get('updateotherreceivers')):
            
            receiver_email = [request.POST['nextownerdetail'],request.POST['ownerdetail'],request.POST['respondentdetail'],request.POST['updateotherreceivers']]
        else:
            receiver_email = [request.POST['nextownerdetail'],request.POST['ownerdetail'],request.POST['respondentdetail']]
        password = "alvvcakmxqbfgvfa"
        message = MIMEMultipart("alternative")
        message["Subject"] = "Exception FollowUp "+str(alertid)
        message["From"] = request.session["username"]
        message["To"] =','.join(receiver_email)   
    
    
        # socks.setdefaultproxy(socks.SOCKS5, 'proxy.', 8080)
        # socks.wrapmodule(smtplib)
        part2 = MIMEText(a, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        # message.attach(part1)
        message.attach(part2)
        if('fp' in request.FILES):
            myfile=request.FILES['fp']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            # print(uploaded_file_url,"djffffffffffffffffffffffffffffffffffff")
            request.session['uploaded_file_url']=uploaded_file_url
            files ="C:/inetpub/wwwroot/iconcept4/media/"+str( request.FILES['fp'] )
            # print("filepath",files)
            # file is the name value which you have provided in form for file field
            # message.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
            # email.send()
            
            with open(files, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(files)
                )
            # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(files)
                message.attach(part)
        
        myid = email.utils.make_msgid()
        # exceptionfilter.CallOver_ID=myid
        message.add_header("In-Reply-To",alertid)
        message.add_header("References", alertid)
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
        # exceptionfilter.save()
        gmail_user = request.session["username"]
        gmail_pwd = 'Iconcept4nbas'
        smtpserver = smtplib.SMTP("""{0}""".format(smtpserver),"""{0}""".format(smtpport))
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        # smtpserver.login('adegokeadeleke.ayo@gmail.com',password)
        smtpserver.sendmail(request.session['username'], to,message.as_string())
    
        smtpserver.close()
    
        print('SUCCESS')
    

        print(sdsignal)
        print(comments)
        print(Id)
        if (sdsignal== 'send'):
            cursor1=connection.cursor()
            cursor1.execute('''                            UPDATE U_IC4INDEP.ALERT_JOURNAL 
                                            SET ALERT_COMMENT = %s
                                         
                                            
                                            WHERE ALERT_ID = %s '''.format(comments,alertid))
            useractivity(request.session.session_key,"Alert Review",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        request.session['username'],today_date,"Sucess","Click",request.session.session_key,"Alert Review",
        """ {0} responded on Follow Up with alert id {1} """.format(request.session['username'],alertid),today,today_date)
            return HttpResponseRedirect(reverse('followupindexall'))
        else:
            cursor1=connection.cursor()
            cursor1.execute('''                            UPDATE U_IC4INDEP.ALERT_JOURNAL 
                                            SET ALERT_COMMENT = %s, 
                                            ACCEPTED_BY = %s
                                            
                                            WHERE ALERT_ID = %s '''.format(comments,request.session['username'],alertid))
            useractivity(request.session.session_key,"Alert Review",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        request.session['username'],today_date,"Sucess","Click",request.session.session_key,"Alert Review",
        """ {0} closed  Follow Up with alert id {1} """.format(request.session['username'],alertid),today,today_date)
            return HttpResponseRedirect(reverse('followupindexall'))        
            
            
  

    else:
        return HttpResponseRedirect(reverse('login'))





def Accept(request):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):

        sdsignal=request.POST['sendSignal']
        today=datetime.now()
        stringDate=today.strftime("%m%d%Y,%H:%M:%S")
        comments=''
        Id=request.POST['id']
        alertid=request.POST['alertid']
        Investigation=request.POST['Investigation']
        prev_comments=request.POST['prevcomments']
        cursor=connection.cursor()
        results=cursor.execute("""SELECT EXCEPTION_DETAIL FROM ALERT_JOURNAL WHERE ALERT_ID= %s """,(alertid))
        # username=cursor.fetchone()
        for result in results:
            FORMAL = str(result[0])
        
        FORMAL.replace('''<style type="text/css">
.alertHeader {
	text-align: center;
	line-height: 30px;
	font-familly: Verdana;
	font-size: 16px;
	color: #333333;
	font-weight: bold;
	width: 100%;
}

.internalControlAlert {
	background-color: #9CCF00;
}

.auditImplication {
	background-color: #0070C0;
}

.action {
	background-color: #319A63;
}

.additional_info {
	background-color: #996d90;
}

.alertLabel {
	line-height: 20px;
	font-familly: Verdana;
	font-size: 12px;
	color: #333333;
	font-weight: bold;
	width: 150px;
}

.alertValue {
	line-height: 20px;
	font-familly: Verdana;
	font-size: 12px;
	color: black;
	width: 100%;
}
</style>''','')
        comments+=prev_comments
        comments+='\n'+ request.session['userparam']
        comments+=' ['+ stringDate + ']: ' + request.POST['comments']
        a="""\
                                             <html lang="en"><head>
                                             <style>body{{margin:0;padding:0;overflow-x:auto!important;overflow-y:hidden!important}}.mail-detail-content{{box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;font-size:13px;font-weight:400;font-feature-settings:"liga" 0;width:100%;position:relative;padding:0}}.ios.smartphone .mail-detail-content{{-webkit-overflow-scrolling:touch;overflow-x:auto}}.smartphone .mail-detail-content{{font-size:15px}}.mail-detail-content>div>[class$="-content"]{{padding:0}}.mail-detail-content.plain-text{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;white-space:pre-wrap}}.mail-detail-content.plain-text blockquote{{white-space:normal}}.mail-detail-content.fixed-width-font,.mail-detail-content.fixed-width-font.plain-text,.mail-detail-content.fixed-width-font blockquote,.mail-detail-content.fixed-width-font.plain-text blockquote,.mail-detail-content.fixed-width-font blockquote p,.mail-detail-content.fixed-width-font.plain-text blockquote p{{font-family:monospace;-webkit-font-feature-settings:normal;font-feature-settings:normal}}.mail-detail-content.simple-mail{{max-width:700px}}.mail-detail-content.simple-mail.big-screen{{max-width:100%}}.mail-detail-content.simple-mail img{{max-width:100%;height:auto!important}}.mail-detail-content img[src=""]{{background-color:rgba(0,0,0,.1);background-image:repeating-linear-gradient(45deg,transparent,transparent 20px,rgba(255,255,255,.5) 20px,rgba(255,255,255,.5) 40px)}}.mail-detail-content p{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;margin:0 0 1em}}.mail-detail-content h1{{font-size:28px}}.mail-detail-content h2{{font-size:21px}}.mail-detail-content h3{{font-size:16.38px}}.mail-detail-content h4{{font-size:14px}}.mail-detail-content h5{{font-size:11.62px}}.mail-detail-content h6{{font-size:9.38px}}.mail-detail-content a{{word-break:break-word;text-decoration:none;color:inherit}}.mail-detail-content a:hover{{color:inherit}}.mail-detail-content a[href]{{color:#3c61aa;text-decoration:underline}}.mail-detail-content th{{padding:8px;text-align:center}}.mail-detail-content th[align=left]{{text-align:left}}.mail-detail-content .calendar-detail .label{{display:block;text-shadow:none;font-weight:400;background-color:transparent}}.mail-detail-content img.emoji-softbank{{margin:0 2px}}.mail-detail-content pre{{word-break:keep-all;word-break:initial;white-space:pre-wrap;background-color:transparent;border:0 none;border-radius:0}}.mail-detail-content table{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;font-size:13px;font-weight:400;font-feature-settings:"liga" 0;line-height:normal;border-collapse:collapse}}.mail-detail-content ul,.mail-detail-content ol{{padding:0;padding-left:16px;margin:1em 0 1em 24px}}.mail-detail-content ul{{list-style-type:disc}}.mail-detail-content ul ul{{list-style-type:circle}}.mail-detail-content ul ul ul{{list-style-type:square}}.mail-detail-content li{{line-height:normal;margin-bottom:.5em}}.mail-detail-content blockquote{{color:#555;font-size:13px;border-left:2px solid #ddd;padding:0 0 0 16px;margin:16px 0}}.mail-detail-content blockquote p{{font-size:13px}}.mail-detail-content blockquote blockquote{{border-color:#283f73;margin:8px 0}}.mail-detail-content.colorQuoted blockquote blockquote{{color:#283f73!important;border-left:2px solid #283f73}}.mail-detail-content.colorQuoted blockquote blockquote a[href]:not(.deep-link){{color:#283f73}}.mail-detail-content.colorQuoted blockquote blockquote a[href]:not(.deep-link):hover{{color:#1b2a4d}}.mail-detail-content.colorQuoted blockquote blockquote blockquote{{color:#dd0880!important;border-left:2px solid #dd0880}}.mail-detail-content.colorQuoted blockquote blockquote blockquote a[href]:not(.deep-link){{color:#dd0880}}.mail-detail-content.colorQuoted blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#ac0663}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote{{color:#8f09c7!important;border-left:2px solid #8f09c7}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote a[href]:not(.deep-link){{color:#8f09c7}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#6c0796}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote{{color:#767676!important;border-left:2px solid #767676}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote a[href]:not(.deep-link){{color:#767676}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#5d5d5d}}.mail-detail-content.disable-links a[href]{{color:#aaa!important;text-decoration:line-through!important;cursor:default!important;pointer-events:none!important}}.mail-detail-content .blockquote-toggle{{color:#767676;font-size:13px;padding-left:56px;margin:16px 0;min-height:16px;word-break:break-word}}.mail-detail-content .blockquote-toggle button.bqt{{color:#696969;background-color:#eee;padding:1px 10px;display:inline-block;font-size:14px;line-height:16px;cursor:pointer;outline:0;position:absolute;left:0;border:0}}.mail-detail-content .blockquote-toggle button.bqt:hover,.mail-detail-content .blockquote-toggle button.bqt:focus{{color:#fff;background-color:#3c61aa;text-decoration:none}}.mail-detail-content .max-size-warning{{color:#767676;padding:16px 16px 0;border-top:1px solid #ddd}}.mail-detail-content a.deep-link{{color:#fff;background-color:#3c61aa;text-decoration:none;font-size:90%;font-weight:700;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif!important;padding:.1em 8px;border-radius:3px}}.mail-detail-content a.deep-link:hover,.mail-detail-content a.deep-link:focus,.mail-detail-content a.deep-link:active{{color:#fff;background-color:#2f4b84}}@media print{{.mail-detail-content .collapsed-blockquote{{display:block!important}}.mail-detail-content .blockquote-toggle{{display:none!important}}.mail-detail-content>div[id*=ox-]>h1,.mail-detail-content>div[id*=ox-]>h2,.mail-detail-content>div[id*=ox-]>h3,.mail-detail-content>div[id*=ox-]>h4,.mail-detail-content>div[id*=ox-]>h5{{margin-top:0}}</style>
                    <style>.mail-detail-content .alertHeader {{ text-align: center; line-height: 30px; font-size: 16px; color: rgb(51, 51, 51); font-weight: bold; width: 100%; }} .mail-detail-content .ControlAlert {{ background-color: rgb(173, 216, 230); }} .mail-detail-content .internalControlAlert {{ background-color: rgb(156, 207, 0); }} .mail-detail-content .auditImplication {{ background-color: rgb(0, 112, 192); }} .mail-detail-content .action {{ background-color: rgb(49, 154, 99); }} .mail-detail-content .additional_info {{ background-color: rgb(153, 109, 144); }} .mail-detail-content .alertLabel {{ line-height: 20px; font-size: 12px; color: rgb(51, 51, 51); font-weight: bold; width: 150px; }} .mail-detail-content .alertValue {{ line-height: 20px; font-size: 12px; color: black; width: 100%; }} .mail-detail-content .cell {{ border: 1px solid black; width: 30%; padding: 5px; text-align: left; }} </style>
        
                    </head>
                    <body class="mail-detail-content noI18n colorQuoted">
        
        
        
                    

                        <table cellspacing="0" cellpadding="0" border="0" width="70%" style="margin:0 auto; margin-top:2rem">
                            <tbody>
                              <tr>
                                <td colspan="2" class="alertHeader auditImplication">COMMENTS
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre style="margin-bottom: 1rem;">{1}</pre>
                                                        
                            </td></tr>
                               
                            
                            <tr>
                                <td colspan="2" class="alertHeader internalControlAlert">TRANSACTION DETAILS
                            </td></tr>
                          
                        
               
                           <tr>
                            <td class="cell">ACCOUNT NUMBER</td>
                            <td class="cell">{3}</td>
                        </tr>
                         <tr>
                            <td class="cell">ACCOUNT NAME</td>
                            <td class="cell">{4}</td>
                        </tr>
                         <tr>
                            <td class="cell">BRANCH CODE</td>
                            <td class="cell">{5}</td>
                        </tr>

                         <tr>
                            <td class="cell">TRANSACTION TYPE</td>
                            <td class="cell">{6}</td>
                        </tr>

                         <tr>
                            <td class="cell">TRANSACTION AMOUNT</td>
                            <td class="cell">{7}</td>
                        </tr>
                      
                        
                         <tr>
                            <td class="cell">TRANSACTION NARRATION</td>
                            <td class="cell">{8}</td>
                        </tr>

                                     <tr>
                            <td class="cell">POSTING DATE</td>
                            <td class="cell">{9}</td>
                        </tr>
                       
                        </tbody></table>
                                                {0}

                            
                        </body></html>        
    """.format(FORMAL,request.POST['comments'],alertid,request.POST.get('accountnumber'),request.POST.get('accountname'),request.POST.get('branchCode'),request.POST.get('transactiontype'),request.POST.get('transactionamount'),request.POST.get('narrative'),request.POST.get('postingdate') )  
        
        b="""\
                               <html>

                                        <style type="text/css">
                                        .alertHeader {
                                            text-align: center;
                                            line-height: 30px;
                                            font-familly: Verdana;
                                            font-size: 16px;
                                            color: #333333;
                                            font-weight: bold;
                                            width: 100%;
                                        }

                                        .internalControlAlert {
                                            background-color: #9CCF00;
                                        }

                                        .auditImplication {
                                            background-color: #0070C0;
                                        }

                                        .action {
                                            background-color: #319A63;
                                        }

                                        .additional_info {
                                            background-color: #996d90;
                                        }

                                        .alertLabel {
                                            line-height: 20px;
                                            font-familly: Verdana;
                                            font-size: 12px;
                                            color: #333333;
                                            font-weight: bold;
                                            width: 150px;
                                        }

                                        .alertValue {
                                            line-height: 20px;
                                            font-familly: Verdana;
                                            font-size: 12px;
                                            color: black;
                                            width: 100%;
                                        }
                                        </style>
                                        <table cellspacing='0' cellpadding='0' border='0' width='100%'>
                                            <tr>
                                                <td colspan='2' class='alertHeader internalControlAlert'><nobr>INTERNAL
                                                CONTROL ALERT</nobr>
                                            </tr>
                                            
                                            <tr>
                                                <td colspan='2'><pre class='alertValue'>This Alert was generated by iConcept4 at   2021-03-18 23:12:55.999 

                                        CUSTOMER FOREIGN TRANSACTION ABOVE 10,000 ON TIPLUS 100 

                                        <table border=1 cellpadding = 3 cellspacing = 1>
                                        <tbody align = "justify" style = "font-family:verdana; font-size: 12; color:black; background-color:999990">


                                        <tr><td>S/NO.</td><td>BRANCH CODE</td><td>BRANCH NAME</td><td>TRANS DATE</td><td>VALUE DATE</td><td>ACCT NUM</td><td>CUSTOMER ACCOUNT NAME</td>
                                        <td>CURRENCY</td><td>DR/CR</td><td>FCY AMOUNT</td><td>EQUIV LCY AMOUNT AMT</td><td>RATE</td><td>SOURCE CODE</td><td>BATCH NO</td><td>MAKER ID</td>
                                        <td>CHECKER ID</td></tr>

                                        <tr><td>  1  </td><td> 100 </td><td>    </td><td> 2020-03-10 00:00:00.0 </td>
                                        <td> 2020-03-10 00:00:00.0 </td><td> 0780000488 </td><td> CENTRAL BANK OF NIGERIA </td><td> NGN </td>
                                        <td> FTC </td> <td>  </td><td> 34,315,915.92 </td><td>  </td><td>  </td>
                                        <td> 1007ctt200700001 </td><td> TAKINLOLU </td><td> AROTIMI </td>
                                        </tr><tr><td>  2  </td><td> 100 </td><td>    </td><td> 2020-03-10 00:00:00.0 </td>
                                        <td> 2020-03-10 00:00:00.0 </td><td> 0780000488 </td><td> CENTRAL BANK OF NIGERIA </td><td> NGN </td>
                                        <td> FTC </td> <td>  </td><td> 161,028,253.92 </td><td>  </td><td>  </td>
                                        <td> 1007ctt200700001 </td><td> TAKINLOLU </td><td> AROTIMI </td>
                                        </tr><tr><td>  3  </td><td> 100 </td><td>    </td><td> 2020-03-10 00:00:00.0 </td>
                                        <td> 2020-03-10 00:00:00.0 </td><td> 0780000457 </td><td> CITI BANK OPERATING USD  A/C </td><td> USD </td>
                                        <td> FTC </td> <td>  </td><td> 102,560,328.14 </td><td>  </td><td>  </td>
                                        <td> 1007ctx200700001 </td><td> OABUSODIQ </td><td> KIMORU </td>
                                        </tr><tr><td>  4  </td><td> 100 </td><td>    </td><td> 2020-03-10 00:00:00.0 </td>
                                        <td> 2020-03-10 00:00:00.0 </td><td> 0780000457 </td><td> CITI BANK OPERATING USD  A/C </td><td> USD </td>
                                        <td> FTC </td> <td>  </td><td> 365,380,000.00 </td><td>  </td><td>  </td>
                                        <td> 1007ctx200700001 </td><td> OABUSODIQ </td><td> KIMORU </td>
                                        </tr><tr><td>  5  </td><td> 100 </td><td>    </td><td> 2020-03-10 00:00:00.0 </td>
                                        <td> 2020-03-10 00:00:00.0 </td><td> 0780000440 </td><td> CITI BANK EXP DOM USD NEW YORK USA </td><td> USD </td>
                                        <td> FTC </td> <td>  </td><td> 10,121,026.00 </td><td>  </td><td>  </td>
                                        <td> 1007cu6200700001 </td><td> SONACHUKWU </td><td> CJACOBS </td>
                                        </tr><tr><td>  6  </td><td> 100 </td><td>    </td><td> 2020-03-10 00:00:00.0 </td>
                                        <td> 2020-03-10 00:00:00.0 </td><td> 0780000440 </td><td> CITI BANK EXP DOM USD NEW YORK USA </td><td> USD </td>
                                        <td> FTC </td> <td>  </td><td> 94,304,782.61 </td><td>  </td><td>  </td>
                                        <td> 1007cvt200700001 </td><td> COSOBASE2 </td><td> COKPECHI1 </td>
                                        </tr><tr><td>  7  </td><td> 100 </td><td>    </td><td> 2020-03-10 00:00:00.0 </td>
                                        <td> 2020-03-10 00:00:00.0 </td><td> 0780000488 </td><td> CENTRAL BANK OF NIGERIA </td><td> NGN </td>
                                        <td> FTC </td> <td>  </td><td> 188,946,645.79 </td><td>  </td><td>  </td>
                                        <td> 1007cyb200700001 </td><td> TAKINLOLU </td><td> AROTIMI </td>
                                        </tr><tr><td>  8  </td><td> 100 </td><td>    </td><td> 2020-03-10 00:00:00.0 </td>
                                        <td> 2020-03-10 00:00:00.0 </td><td> 0780000440 </td><td> CITI BANK EXP DOM USD NEW YORK USA </td><td> USD </td>
                                        <td> FTC </td> <td>  </td><td> 365,380,000.00 </td><td>  </td><td>  </td>
                                        <td> 1007cz3200700001 </td><td> OOLAKUNORI </td><td> CEBHOHIMEN </td>
                                        </tr><tr><td>  9  </td><td> 100 </td><td>    </td><td> 2020-03-10 00:00:00.0 </td>
                                        <td> 2020-03-10 00:00:00.0 </td><td> 0780000488 </td><td> CENTRAL BANK OF NIGERIA </td><td> NGN </td>
                                        <td> FTC </td> <td>  </td><td> 73,571,243.59 </td><td>  </td><td>  </td>
                                        <td> 1007czj200700001 </td><td> TAKINLOLU </td><td> AROTIMI </td>
                                        </tr><tr><td>  10  </td><td> 100 </td><td>    </td><td> 2020-03-10 00:00:00.0 </td>
                                        <td> 2020-03-10 00:00:00.0 </td><td> 0780000488 </td><td> CENTRAL BANK OF NIGERIA </td><td> NGN </td>
                                        <td> FTC </td> <td>  </td><td> 133,160,043.19 </td><td>  </td><td>  </td>
                                        <td> 1007czj200700001 </td><td> TAKINLOLU </td><td> AROTIMI </td>
                                        </tr>

                                        </tbody>
                                        </table>

                                        This link to Investigation: <a href=https://127.0.0.1:3034/iConcept4?startup=iConcept4&form=C4InvestigationUI&q=ALERT_ID%20LIKE%20%27ALERT20210318111255972%25%27%20AND%20NVL%28ACCEPTED_BY%2C%27null%27%29%3D%27null%27>Click to confirm</a>

                                        This link to Follow Up: <a href=https://127.0.0.1:3034/iConcept4?startup=iConcept4&form=C4RiskAssesmentManagerUI&q=ALERT_ID%20LIKE%20%27ALERT20210318111255972%25%27%20AND%20NVL%28ACCEPTED_BY%2C%27null%27%29%3D%27null%27> Click here to Follow Up</a></pre>
                                            </tr>
                                            <tr>
                                                <td colspan='2' class='alertHeader auditImplication'><nobr>AUDIT
                                                IMPLICATION</nobr>
                                            </tr>
                                            <tr>
                                                <td colspan='2'><pre class='alertValue'>1. To avoid funds diversion or fraudulent activities on the account.</pre>
                                                <td>
                                            </tr>
                                            <tr>
                                                <td colspan='2' class='alertHeader action'>ACTION
                                            </tr>
                                            <tr>
                                                <td colspan='2'><pre class='alertValue'>1. Investigate the transaction to why account is in debit.</pre>
                                                <td>
                                            </tr>
                                            <tr>
                                                <td colspan='2' class='alertHeader additional_info'>ADDITIONAL
                                                INFORMATION
                                                <td>
                                            </tr>
                                            <tr>
                                                <td colspan='2'><pre class='alertValue'></pre>
                                                <td>
                                            </tr>
                                        </table>

                                        </html>        
                                            """  
                                  
        sender_email = "adegokeadeleke.ayo@gmail.com"
        nxtyes='no'
        if(request.POST.get('nextrespondentdetail')):
            print("yes")
            nxtyes='yes'
        
            nxtyes=request.session['username']
        nxtnot='no'
        if(request.POST.get('nextnotifierdetail')):
            print("yes")
        if (nxtnot=='no'):
            nxtnot=request.session['username']
        receiver_email = [request.POST['ownerdetail'],request.POST['nextownerdetail'],request.POST['respondentdetail'],nxtyes,nxtnot]
        password = "alvvcakmxqbfgvfa"
        message = MIMEMultipart("alternative")
        message["Subject"] = "Exception Investigation "+str(alertid)
        message["From"] = request.session["username"]
        message["To"] =','.join(receiver_email)   
    
    
        # socks.setdefaultproxy(socks.SOCKS5, 'proxy.', 8080)
        # socks.wrapmodule(smtplib)
        part2 = MIMEText(a, "html")
        # part3= MIMEText(b, "html")
        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        # message.attach(part1)
        # message.attach(part2)
        if('fp' in request.FILES):
            myfile=request.FILES['fp']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            # print(uploaded_file_url,"djffffffffffffffffffffffffffffffffffff")
            request.session['uploaded_file_url']=uploaded_file_url
            files ="C:/Adroitdeveloments/iconcept4/media/"+str( request.FILES['fp'] )
            # print("filepath",files)
            # file is the name value which you have provided in form for file field
            # message.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)
            # email.send()
            
            with open(files, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(files)
                )
            # After the file is closed
                part['Content-Disposition'] = 'attachment; filename="%s"' % basename(files)
                message.attach(part)
        
        message.attach(part2)
        # message.attach(part3)
        myid = email.utils.make_msgid()
        # exceptionfilter.CallOver_ID=myid
        message.add_header("In-Reply-To",Id)
        message.add_header("References", Id)
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
        # exceptionfilter.save()
        gmail_user = request.session["username"]
        gmail_pwd = 'Iconcept4nbas'
        smtpserver = smtplib.SMTP("""{0}""".format(smtpserver),"""{0}""".format(smtpport))
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        # smtpserver.login('adegokeadeleke.ayo@gmail.com',password)
        smtpserver.sendmail(request.session['username'], to,message.as_string())
    
        smtpserver.close()
    
        print('SUCCESS')
    

        print(sdsignal)
        print(comments)
        print(Id)
        if (sdsignal== 'send'):
            cursor1=connection.cursor()
            cursor1.execute(''' UPDATE U_IC4INDEP.ALERT_DETAILS 
                                SET ALERT_COMMENTS = %s, 
                                INVESTIGATION = %s
                                WHERE ID = %s '''.format(comments,Investigation,Id))
            useractivity(request.session.session_key,"Alert Review",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        request.session['username'],today_date,"Sucess","Click",request.session.session_key,"Alert Review",
        """ {0} responded on Alert Review with alert id {1} """.format(request.session['username'],alertid),today,today_date)
        
            return HttpResponseRedirect(reverse('alertreviewindexall'))
        else:
            cursor1=connection.cursor()
            cursor1.execute(''' UPDATE U_IC4INDEP.ALERT_DETAILS 
                                SET ALERT_COMMENTS = %s, 
                                ACCEPTED_BY = %s, 
                                INVESTIGATION = %s
                                WHERE ID = %s '''.format(comments,request.session['username'],Investigation,Id))
            useractivity(request.session.session_key,"Alert Review",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        request.session['username'],today_date,"Sucess","Click",request.session.session_key,"Alert Review",
        """ {0} closed on Alert Review with alert id {1} """.format(request.session['username'],alertid),today,today_date)
            return HttpResponseRedirect(reverse('alertreviewindexall'))
            # return HttpResponseRedirect(reverse('alertreviewindex',args=(),kwargs={'id':alertid}))        
            
            
  

    else:
        return HttpResponseRedirect(reverse('login'))

      

   
               





















