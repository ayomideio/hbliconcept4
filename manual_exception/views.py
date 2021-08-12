import string
import random
from django.core.mail import send_mail, get_connection
import numpy as np
from datetime import date
from datetime import timedelta
import json
from iconcept4.views import returnallbranch, useractivity
from django.core.files.storage import FileSystemStorage
from email.mime.application import MIMEApplication
from io import BytesIO


import requests
import time

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, query
from os.path import basename
import os

from iconcept4.models import *

from django.http import HttpResponseRedirect, HttpResponse, HttpResponseRedirect, JsonResponse
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
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.utils

import socket
from datetime import datetime
today = datetime.date(datetime.now())
date_time = datetime.now()
BASEDIR = ""
# 172.27.4.4 80
today = datetime.date(datetime.now())
date_time = datetime.now()
from iconcept4.views import dictfetchall


def random_string(letter_count, digit_count):
    str1 = ''.join((random.choice(string.ascii_letters)
                   for x in range(letter_count)))
    str1 += ''.join((random.choice(string.digits) for x in range(digit_count)))

    sam_list = list(str1)  # it converts the string to list.
    # It uses a random.shuffle() function to shuffle the string.
    random.shuffle(sam_list)
    final_string = ''.join(sam_list)
    return final_string


branch_cd = "0"


def index(request, id):
    request.session.set_expiry(60*25)
    if('userparam' in request.session):

        b_c = ''

        b_c = returnallbranch(
            request.session['secondarybranch'], request.session['username'])
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
 
                                                ''',{'username1':request.session['username'],'username2':request.session['username'],'alertid':id})

        yList = dictfetchall(cursor)

        columns = [col[0] for col in cursor.description]
        # print(yList)
        # profiles = IC4_Profile.objects.all()

        profiles = Profile.objects.all()

        return render(request, 'InvestigationManagerGrid.html', {'results': yList, 'Profiles': profiles, 'username': request.session['userparam'], 'grouplist': request.session['grouplist'], 'grouplistbsm': request.session['grouplistbsm'], 'grouplistbc': request.session['grouplistbc'], 'grouplisttrs': request.session['grouplisttrs'], 'grouplisttrc': request.session['grouplisttrc'], 'grouplistcon': request.session['grouplistcon'], 'grouplistfot': request.session['grouplistfot'], 'grouplistfoc': request.session['grouplistfoc'], 'grouplist_ce': request.session['grouplist_ce'], 'grouplist_ca': request.session['grouplist_ca'], 'grouplist_db': request.session['grouplist_db'], 'grouplist_ei': request.session['grouplist_ei'], 'grouplist_report': request.session['grouplistreport']})
    else:
        return HttpResponseRedirect(reverse('login'))


def indexall(request):
    request.session.set_expiry(60*25)
    if('userparam' in request.session):

        b_c = ''
        username = request.session['userparam']
        pbranch = request.session['secondarybranch']
        today_date = datetime.date(datetime.now())

        b_c = returnallbranch(
            request.session['secondarybranch'], request.session['username'])
        print(b_c)
        cursor = connection.cursor()
        result = cursor.execute('''
                                                          
SELECT * FROM (select /*+ FIRST_ROWS(20) */ a.*, ROWNUM ROWNO FROM (SELECT * FROM (SELECT ID, EXCEPTION_ID, EXCEPTION_TITLE, RECIPIENT, RECIPIENT_EMAIL, BRANCH_CODE, SEVERITY_LEVEL, ADDITIONAL_RECIPIENTS, 
                            CONTROL_PROCESS, REVIEW_DATE, EXCEPTION_STATUS, EXCEPTION_DATE, EXCEPTION_OWNER, IC4_INPUTTER, ACCEPT_DATE, TO_CHAR(OBSERVATION)OBSERVATION, TO_CHAR(EXCEPTION_DETAIL)EXCEPTION_DETAIL, 
                            TO_CHAR(IMPLICATION)IMPLICATION, TO_CHAR(ACTION)ACTION, TO_CHAR(RECOMMENDATION)RECOMMENDATION, TO_CHAR(IC4_REASON)IC4_REASON, IC4_SEVERITY_ID 
                            FROM U_IC4INDEP.MANUAL_EXCEPTION  
                            WHERE EXCEPTION_STATUS <> 'ACCEPTED' 
                            AND (IC4_INPUTTER IN %(username1)s OR RECIPIENT_EMAIL IN %(username1)s OR EXCEPTION_OWNER IN %(username1)s OR SUPERVISOR IN %(username1)s
                            OR OTHER_RECEIVER IN %(username1)s OR IC4_REASON IS NULL OR TO_CHAR(IC4_REASON) IN %(username1)s) 
                            AND (EXCEPTION_STATUS = 'RESPONSE' OR EXCEPTION_STATUS = 'ESCALATED') ORDER BY ID DESC) a ) a  ) b

UNION

SELECT * FROM (select /*+ FIRST_ROWS(20) */ a.*, ROWNUM ROWNO FROM (SELECT * FROM (SELECT ID, EXCEPTION_ID, EXCEPTION_TITLE, RECIPIENT, RECIPIENT_EMAIL, BRANCH_CODE, SEVERITY_LEVEL, ADDITIONAL_RECIPIENTS, 
                            CONTROL_PROCESS, REVIEW_DATE, EXCEPTION_STATUS, EXCEPTION_DATE, EXCEPTION_OWNER, IC4_INPUTTER, ACCEPT_DATE, TO_CHAR(OBSERVATION)OBSERVATION, TO_CHAR(EXCEPTION_DETAIL)EXCEPTION_DETAIL, 
                            TO_CHAR(IMPLICATION)IMPLICATION, TO_CHAR(ACTION)ACTION, TO_CHAR(RECOMMENDATION)RECOMMENDATION, TO_CHAR(IC4_REASON)IC4_REASON, IC4_SEVERITY_ID 
                            FROM U_IC4INDEP.MANUAL_EXCEPTION  
                            WHERE EXCEPTION_STATUS <> 'ACCEPTED' 
                            AND (IC4_INPUTTER IN %(username2)s OR RECIPIENT_EMAIL IN %(username2)s OR EXCEPTION_OWNER IN %(username2)s OR SUPERVISOR IN %(username2)s
                            OR OTHER_RECEIVER IN %(username2)s OR IC4_REASON IS NULL OR TO_CHAR(IC4_REASON) IN %(username2)s) 
                            AND (EXCEPTION_STATUS = 'RESPONSE' OR EXCEPTION_STATUS = 'ESCALATED') ORDER BY ID DESC) a ) a  ) b
 
                                                ''',{'username1':request.session['username']+';','username2':request.session['username']})

        yList = dictfetchall(cursor)
        uploaded_file_url = ''
        if('uploaded_file_url' in request.session):
            uploaded_file_url = request.session['uploaded_file_url']
        controlpro = cursor.execute(''' SELECT * FROM U_IC4INDEP.MANUAL_OBSERVATION 
                    ORDER BY DESCRIPTION ASC ''')
        controlprocess = dictfetchall(cursor)
        columns = [col[0] for col in cursor.description]
        # print(yList)
        # profiles = IC4_Profile.objects.all()

        profiles = Profile.objects.all()

        return render(request, 'ManualExceptionGrid.html', {'date': today.strftime("%b-%d-%Y"), 'manualexceptionid': "MAEX -"+today.strftime("%b-%d-%Y")+random_string(13, 7), 'uploaded_file_url': uploaded_file_url, 'calloverurl': request.session['calloverurl'], 'controlprocess': controlprocess, 'results': yList, 'Profiles': profiles, 'username': request.session['userparam'], 'grouplist': request.session['grouplist'], 'grouplistbsm': request.session['grouplistbsm'], 'grouplistbc': request.session['grouplistbc'], 'grouplisttrs': request.session['grouplisttrs'], 'grouplisttrc': request.session['grouplisttrc'], 'grouplistcon': request.session['grouplistcon'], 'grouplistfot': request.session['grouplistfot'], 'grouplistfoc': request.session['grouplistfoc'], 'grouplist_ce': request.session['grouplist_ce'], 'grouplist_ca': request.session['grouplist_ca'], 'grouplist_db': request.session['grouplist_db'], 'grouplist_ei': request.session['grouplist_ei'], 'grouplist_report': request.session['grouplistreport']})
    else:
        return HttpResponseRedirect(reverse('login'))


def Followup_Detail(request):
    request.session.set_expiry(60*25)
    callover_id = 'ALERT20210319083620355'
    if('userparam' in request.session):

        request.session['arraytest'] = ""
        prev_comments = request.POST['prevcomments']
        today = datetime.now()
        stringDate = today.strftime("%m%d%Y,%H:%M:%S")
        comments = ''
        comments += prev_comments
        comments += '\n' + request.session['username']
        comments += ' [' + stringDate + ']: ' + request.POST['comments']

        cursor = connection.cursor()

        cursor.execute(''' UPDATE MANUAL_EXCEPTION
                                SET IC4_REASON = %s
                                WHERE EXCEPTION_ID = %s  '''.format(request.session['username'], callover_id))
        # callover_id="CEZIAKONWA202101070700000010CHDP210070027"
        request.session['selectedbranch'] = callover_id
        isOwner = 'YES'

        yList = dictfetchall(cursor)
        # print(yList)

        module = 'Callover for Teller'
        today = date.today()

        return render(request, 'followup.html', {'date': today.strftime("%b-%d-%Y"), 'manualexceptionid': "MAEX -"+today.strftime("%b-%d-%Y")+random_string(13, 7), 'results': yList, 'isOwner': isOwner, 'username': request.session['userparam'], 'grouplist': request.session['grouplist'], 'grouplistbsm': request.session['grouplistbsm'], 'grouplistbc': request.session['grouplistbc'], 'grouplisttrs': request.session['grouplisttrs'], 'grouplisttrc': request.session['grouplisttrc'], 'grouplistcon': request.session['grouplistcon'], 'grouplistfot': request.session['grouplistfot'], 'grouplistfoc': request.session['grouplistfoc'], 'grouplist_ce': request.session['grouplist_ce'], 'grouplist_ca': request.session['grouplist_ca'], 'grouplist_db': request.session['grouplist_db'], 'grouplist_ei': request.session['grouplist_ei'], 'grouplist_report': request.session['grouplistreport']})

    else:

        return HttpResponseRedirect(reverse('login'))


def clickfromMail(request, calloverid):
    request.session.set_expiry(60*25)
    if('userparam' in request.session):

        b_c = ''
        username = request.session['userparam']
        pbranch = request.session['secondarybranch']
        today_date = datetime.date(datetime.now())

        b_c = returnallbranch(
            request.session['secondarybranch'], request.session['username'])
        print(b_c)
        cursor = connection.cursor()
        useractivity(request.session.session_key, "Manual Exception", socket.gethostbyname(socket.gethostname()), socket.gethostname(),
                     request.session['username'], today_date, "Sucess", "Click", request.session.session_key, "Manual Exception",
                     """ {0} clicked on a manual exception with manual exception id {1} """.format(request.session['username'], calloverid), today, today_date)

        result = cursor.execute('''
               
              SELECT * FROM ( (select /*+ FIRST_ROWS(20) */ a.*, ROWNUM ROWNO FROM (SELECT * FROM (SELECT ID, EXCEPTION_ID, EXCEPTION_TITLE, RECIPIENT, RECIPIENT_EMAIL, BRANCH_CODE, SEVERITY_LEVEL, ADDITIONAL_RECIPIENTS, 
                            CONTROL_PROCESS, REVIEW_DATE, EXCEPTION_STATUS, EXCEPTION_DATE, EXCEPTION_OWNER, IC4_INPUTTER, ACCEPT_DATE, TO_CHAR(OBSERVATION), TO_CHAR(EXCEPTION_DETAIL), TO_CHAR(IMPLICATION), TO_CHAR(ACTION), TO_CHAR(RECOMMENDATION), TO_CHAR(IC4_REASON), IC4_SEVERITY_ID 
                            FROM U_IC4INDEP.MANUAL_EXCEPTION  
                            WHERE EXCEPTION_STATUS <> 'ACCEPTED' 
                            AND (IC4_INPUTTER IN %(username1)s OR RECIPIENT_EMAIL IN %(username1)s OR EXCEPTION_OWNER IN %(username1)s OR SUPERVISOR IN %(username1)s
                            OR OTHER_RECEIVER IN %(username1)s OR IC4_REASON IS NULL OR TO_CHAR(IC4_REASON) IN %(username1)s) 
                            AND EXCEPTION_ID=%(calloverid)s
                            AND (EXCEPTION_STATUS = 'RESPONSE' OR EXCEPTION_STATUS = 'ESCALATED') ) a ) a  ) 
                
                UNION 
                                            
                (select /*+ FIRST_ROWS(20) */ a.*, ROWNUM ROWNO FROM (SELECT * FROM (SELECT ID, EXCEPTION_ID, EXCEPTION_TITLE, RECIPIENT, RECIPIENT_EMAIL, BRANCH_CODE, SEVERITY_LEVEL, ADDITIONAL_RECIPIENTS, 
                            CONTROL_PROCESS, REVIEW_DATE, EXCEPTION_STATUS, EXCEPTION_DATE, EXCEPTION_OWNER, IC4_INPUTTER, ACCEPT_DATE, TO_CHAR(OBSERVATION), TO_CHAR(EXCEPTION_DETAIL), TO_CHAR(IMPLICATION), TO_CHAR(ACTION), TO_CHAR(RECOMMENDATION), TO_CHAR(IC4_REASON), IC4_SEVERITY_ID 
                            FROM U_IC4INDEP.MANUAL_EXCEPTION  
                            WHERE EXCEPTION_STATUS <> 'ACCEPTED' 
                            AND (IC4_INPUTTER IN %(username2)s OR RECIPIENT_EMAIL IN %(username2)s OR EXCEPTION_OWNER IN %(username2)s OR SUPERVISOR IN %(username2)s
                            OR OTHER_RECEIVER IN %(username2)s OR IC4_REASON IS NULL OR TO_CHAR(IC4_REASON) IN %(username2)s) 
                            AND EXCEPTION_ID= %(calloverid)s
                            AND (EXCEPTION_STATUS = 'RESPONSE' OR EXCEPTION_STATUS = 'ESCALATED') ) a ) a  )
                  ) ORDER BY ID DESC
               
                ''',{'username1':request.session['username']+';','username2':request.session['username'],'calloverid': calloverid})

        yList = dictfetchall(cursor)

        columns = [col[0] for col in cursor.description]
        print(yList)
        # profiles = IC4_Profile.objects.all()

        profiles = Profile.objects.all()

        return render(request, 'ManualExceptionGrid.html', {'results': yList, 'Profiles': profiles, 'test': branch_cd, 'username': request.session['userparam'], 'grouplist': request.session['grouplist'], 'grouplistbsm': request.session['grouplistbsm'], 'grouplistbc': request.session['grouplistbc'], 'grouplisttrs': request.session['grouplisttrs'], 'grouplisttrc': request.session['grouplisttrc'], 'grouplistcon': request.session['grouplistcon'], 'grouplistfot': request.session['grouplistfot'], 'grouplistfoc': request.session['grouplistfoc'], 'grouplist_ce': request.session['grouplist_ce'], 'grouplist_ca': request.session['grouplist_ca'], 'grouplist_db': request.session['grouplist_db'], 'grouplist_ei': request.session['grouplist_ei'], 'grouplist_report': request.session['grouplistreport']})
    else:
        return HttpResponseRedirect(reverse('login'))


# @staff_member_required
def Exception_Detail(request, callover_id):
    request.session.set_expiry(60*25)
    if('userparam' in request.session):

        request.session['arraytest'] = ""

        cursor = connection.cursor()

        cursor.execute(''' SELECT * FROM ( select /*+ FIRST_ROWS(20) */ a.*, ROWNUM ROWNO FROM (SELECT * FROM (SELECT ID, EXCEPTION_ID, EXCEPTION_TITLE, RECIPIENT, RECIPIENT_EMAIL, BRANCH_CODE, SEVERITY_LEVEL, ADDITIONAL_RECIPIENTS, 
                            CONTROL_PROCESS, REVIEW_DATE, EXCEPTION_STATUS, EXCEPTION_DATE, EXCEPTION_OWNER, IC4_INPUTTER, ACCEPT_DATE, TO_CHAR(OBSERVATION), TO_CHAR(EXCEPTION_DETAIL), TO_CHAR(IMPLICATION), TO_CHAR(ACTION), TO_CHAR(RECOMMENDATION), TO_CHAR(IC4_REASON), IC4_SEVERITY_ID 
                            FROM U_IC4INDEP.MANUAL_EXCEPTION  
                            WHERE EXCEPTION_STATUS <> 'ACCEPTED' 
                            AND (IC4_INPUTTER IN %(username1)s OR RECIPIENT_EMAIL IN %(username1)s OR EXCEPTION_OWNER IN %(username1)s OR SUPERVISOR IN %(username1)s
                            OR OTHER_RECEIVER IN %(username1)s OR IC4_REASON IS NULL OR TO_CHAR(IC4_REASON) IN %(username1)s) 
                            AND (EXCEPTION_STATUS = 'RESPONSE' OR EXCEPTION_STATUS = 'ESCALATED') ORDER BY ID DESC) a ) a  ) b 
                            WHERE EXCEPTION_ID=%(calloverid)s
                            
               UNION
               
SELECT * FROM (select /*+ FIRST_ROWS(20) */ a.*, ROWNUM ROWNO FROM (SELECT * FROM (SELECT ID, EXCEPTION_ID, EXCEPTION_TITLE, RECIPIENT, RECIPIENT_EMAIL, BRANCH_CODE, SEVERITY_LEVEL, ADDITIONAL_RECIPIENTS, 
                            CONTROL_PROCESS, REVIEW_DATE, EXCEPTION_STATUS, EXCEPTION_DATE, EXCEPTION_OWNER, IC4_INPUTTER, ACCEPT_DATE, TO_CHAR(OBSERVATION), TO_CHAR(EXCEPTION_DETAIL), TO_CHAR(IMPLICATION), TO_CHAR(ACTION), TO_CHAR(RECOMMENDATION), TO_CHAR(IC4_REASON), IC4_SEVERITY_ID 
                            FROM U_IC4INDEP.MANUAL_EXCEPTION  
                            WHERE EXCEPTION_STATUS <> 'ACCEPTED' 
                            AND (IC4_INPUTTER IN %(username2)s OR RECIPIENT_EMAIL IN %(username2)s OR EXCEPTION_OWNER IN %(username2)s OR SUPERVISOR IN %(username2)s
                            OR OTHER_RECEIVER IN %(username2)s OR IC4_REASON IS NULL OR TO_CHAR(IC4_REASON) IN %(username2)s) 
                            AND (EXCEPTION_STATUS = 'RESPONSE' OR EXCEPTION_STATUS = 'ESCALATED') ORDER BY ID DESC) a ) a  ) b
                            WHERE EXCEPTION_ID=%(calloverid)s
                                               ''',{'username1':request.session['username']+';','username2':request.session['username'],'calloverid': callover_id})

        # callover_id="CEZIAKONWA202101070700000010CHDP210070027"
        request.session['selectedbranch'] = ''+callover_id
        isOwner = 'YES'

        yList = dictfetchall(cursor)
        # print(yList)

        cursor.execute(''' SELECT * FROM U_IC4INDEP.MANUAL_OBSERVATION 
                    ORDER BY DESCRIPTION ASC ''')
        controlprocess = dictfetchall(cursor)

        module = 'Callover for Teller'

        return render(request, 'editmanualexception.html', {'controlprocess': controlprocess, 'results': yList, 'isOwner': isOwner, 'username': request.session['userparam'], 'grouplist': request.session['grouplist'], 'grouplistbsm': request.session['grouplistbsm'], 'grouplistbc': request.session['grouplistbc'], 'grouplisttrs': request.session['grouplisttrs'], 'grouplisttrc': request.session['grouplisttrc'], 'grouplistcon': request.session['grouplistcon'], 'grouplistfot': request.session['grouplistfot'], 'grouplistfoc': request.session['grouplistfoc'], 'grouplist_ce': request.session['grouplist_ce'], 'grouplist_ca': request.session['grouplist_ca'], 'grouplist_db': request.session['grouplist_db'], 'grouplist_ei': request.session['grouplist_ei'], 'grouplist_report': request.session['grouplistreport']})

    else:

        return HttpResponseRedirect(reverse('login'))


def CreateManualException(request):
    request.session.set_expiry(60*25)
    if('userparam' in request.session):

        sdsignal = 'send'

        print(sdsignal)
        today = datetime.now()
        if (sdsignal == 'send'):

            cursor1 = connection.cursor()
            exceptionid = request.POST['manualexceptionid']
            exceptiontitle = request.POST['exceptiontitle']
            recipient = request.POST['recipient']
            recipientemail = request.POST['recipientemail']
            branchcode = '000'
            print("severreeeeeeeeeeeeeeeee",
                  request.POST.get('additionalrecipients'))
            severitylevel = request.POST.get('severitylevel')
            if ('otherreceivers' in request.POST):
                additionalrecipients = request.POST.get('additionalrecipients')
            else:
                additionalrecipients = request.session['username']

            reviewdate = today.strftime("%m%d%Y,%H:%M:%S")
            controlprocess = request.POST['grouping']
            # observation=request.POST['observation']
            exceptiondetail = request.POST['exceptiondetail']
            implication = request.POST.get('implication')
            action = request.POST.get('action')
            if ('otherreceivers' in request.POST):
                exceptionowner = request.POST.get('owner')
            else:
                exceptionowner = request.session['username']
            # exceptionowner=request.POST.get('owner')
            acceptdate = request.POST.get('acceptdate')

            currency = request.POST.get('currency')
            if ('otherreceivers' in request.POST):
                otherreceiver = request.POST.get('otherreceivers')
            else:
                otherreceiver = request.session['username']
            supervisor = request.POST.get('supervisor')
            receiver_email = 'mickkyolaoye@gmail.com'
            observation = request.POST.get('mexobservation')
            recommendation = request.POST.get('mexrecommendation')
            exceptionstatus = 'ESCALATED'
            inputter = request.session['username']
            exceptiondate = today.strftime("%m%d%Y,%H:%M:%S")
            amount = request.POST.get('mexamount')
            if ('fp' in request.FILES):
                myfile = request.FILES['fp']

            cursor1.execute("""   INSERT INTO MANUAL_EXCEPTION
                            ( EXCEPTION_ID, EXCEPTION_TITLE, RECIPIENT, RECIPIENT_EMAIL, BRANCH_CODE, SEVERITY_LEVEL,
                             ADDITIONAL_RECIPIENTS, REVIEW_DATE, CONTROL_PROCESS, 
                            OBSERVATION, EXCEPTION_DETAIL, IMPLICATION, ACTION, RECOMMENDATION, 
                            EXCEPTION_STATUS, IC4_INPUTTER, EXCEPTION_DATE, EXCEPTION_OWNER, 
                            AMOUNT, CURRENCY, OTHER_RECEIVER, SUPERVISOR )
                            VALUES
                            (
                            %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                            %s, %s, %s, %s, %s,
                            %s, %s, %s, %s,
                            %s, %s, %s, %s
                        )""",
                            exceptionid, exceptiontitle, recipient, receiver_email, branchcode, severitylevel,
                            additionalrecipients, reviewdate, controlprocess, observation, exceptiondetail, implication,
                            action, recommendation, exceptionstatus, inputter, exceptiondate, exceptionowner, amount, currency, otherreceiver, supervisor
                            )
            cursor1.execute('''commit ''')
            today = datetime.date(datetime.now())
            date_time = datetime.now()
            useractivity(request.session.session_key, "Manual Exception", socket.gethostbyname(socket.gethostname()), socket.gethostname(),
                         request.session['username'], today_date, "Sucess", "Click", request.session.session_key, "Manual Exception",
                         """ {0} created  manual exception with manual exception id {1} """.format(request.session['username'], exceptionid), today, today)

            today = datetime.now()
            stringDate = today.strftime("%m%d%Y,%H:%M:%S")

            a = """\
                                                <html lang="en"><head><style>body{{margin:0;padding:0;overflow-x:auto!important;overflow-y:hidden!important}}.mail-detail-content{{box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;font-size:13px;font-weight:400;font-feature-settings:"liga" 0;width:100%;position:relative;padding:0}}.ios.smartphone .mail-detail-content{{-webkit-overflow-scrolling:touch;overflow-x:auto}}.smartphone .mail-detail-content{{font-size:15px}}.mail-detail-content>div>[class$="-content"]{{padding:0}}.mail-detail-content.plain-text{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;white-space:pre-wrap}}.mail-detail-content.plain-text blockquote{{white-space:normal}}.mail-detail-content.fixed-width-font,.mail-detail-content.fixed-width-font.plain-text,.mail-detail-content.fixed-width-font blockquote,.mail-detail-content.fixed-width-font.plain-text blockquote,.mail-detail-content.fixed-width-font blockquote p,.mail-detail-content.fixed-width-font.plain-text blockquote p{{font-family:monospace;-webkit-font-feature-settings:normal;font-feature-settings:normal}}.mail-detail-content.simple-mail{{max-width:700px}}.mail-detail-content.simple-mail.big-screen{{max-width:100%}}.mail-detail-content.simple-mail img{{max-width:100%;height:auto!important}}.mail-detail-content img[src=""]{{background-color:rgba(0,0,0,.1);background-image:repeating-linear-gradient(45deg,transparent,transparent 20px,rgba(255,255,255,.5) 20px,rgba(255,255,255,.5) 40px)}}.mail-detail-content p{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;margin:0 0 1em}}.mail-detail-content h1{{font-size:28px}}.mail-detail-content h2{{font-size:21px}}.mail-detail-content h3{{font-size:16.38px}}.mail-detail-content h4{{font-size:14px}}.mail-detail-content h5{{font-size:11.62px}}.mail-detail-content h6{{font-size:9.38px}}.mail-detail-content a{{word-break:break-word;text-decoration:none;color:inherit}}.mail-detail-content a:hover{{color:inherit}}.mail-detail-content a[href]{{color:#3c61aa;text-decoration:underline}}.mail-detail-content th{{padding:8px;text-align:center}}.mail-detail-content th[align=left]{{text-align:left}}.mail-detail-content .calendar-detail .label{{display:block;text-shadow:none;font-weight:400;background-color:transparent}}.mail-detail-content img.emoji-softbank{{margin:0 2px}}.mail-detail-content pre{{word-break:keep-all;word-break:initial;white-space:pre-wrap;background-color:transparent;border:0 none;border-radius:0}}.mail-detail-content table{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;font-size:13px;font-weight:400;font-feature-settings:"liga" 0;line-height:normal;border-collapse:collapse}}.mail-detail-content ul,.mail-detail-content ol{{padding:0;padding-left:16px;margin:1em 0 1em 24px}}.mail-detail-content ul{{list-style-type:disc}}.mail-detail-content ul ul{{list-style-type:circle}}.mail-detail-content ul ul ul{{list-style-type:square}}.mail-detail-content li{{line-height:normal;margin-bottom:.5em}}.mail-detail-content blockquote{{color:#555;font-size:13px;border-left:2px solid #ddd;padding:0 0 0 16px;margin:16px 0}}.mail-detail-content blockquote p{{font-size:13px}}.mail-detail-content blockquote blockquote{{border-color:#283f73;margin:8px 0}}.mail-detail-content.colorQuoted blockquote blockquote{{color:#283f73!important;border-left:2px solid #283f73}}.mail-detail-content.colorQuoted blockquote blockquote a[href]:not(.deep-link){{color:#283f73}}.mail-detail-content.colorQuoted blockquote blockquote a[href]:not(.deep-link):hover{{color:#1b2a4d}}.mail-detail-content.colorQuoted blockquote blockquote blockquote{{color:#dd0880!important;border-left:2px solid #dd0880}}.mail-detail-content.colorQuoted blockquote blockquote blockquote a[href]:not(.deep-link){{color:#dd0880}}.mail-detail-content.colorQuoted blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#ac0663}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote{{color:#8f09c7!important;border-left:2px solid #8f09c7}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote a[href]:not(.deep-link){{color:#8f09c7}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#6c0796}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote{{color:#767676!important;border-left:2px solid #767676}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote a[href]:not(.deep-link){{color:#767676}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#5d5d5d}}.mail-detail-content.disable-links a[href]{{color:#aaa!important;text-decoration:line-through!important;cursor:default!important;pointer-events:none!important}}.mail-detail-content .blockquote-toggle{{color:#767676;font-size:13px;padding-left:56px;margin:16px 0;min-height:16px;word-break:break-word}}.mail-detail-content .blockquote-toggle button.bqt{{color:#696969;background-color:#eee;padding:1px 10px;display:inline-block;font-size:14px;line-height:16px;cursor:pointer;outline:0;position:absolute;left:0;border:0}}.mail-detail-content .blockquote-toggle button.bqt:hover,.mail-detail-content .blockquote-toggle button.bqt:focus{{color:#fff;background-color:#3c61aa;text-decoration:none}}.mail-detail-content .max-size-warning{{color:#767676;padding:16px 16px 0;border-top:1px solid #ddd}}.mail-detail-content a.deep-link{{color:#fff;background-color:#3c61aa;text-decoration:none;font-size:90%;font-weight:700;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif!important;padding:.1em 8px;border-radius:3px}}.mail-detail-content a.deep-link:hover,.mail-detail-content a.deep-link:focus,.mail-detail-content a.deep-link:active{{color:#fff;background-color:#2f4b84}}@media print{{.mail-detail-content .collapsed-blockquote{{display:block!important}}.mail-detail-content .blockquote-toggle{{display:none!important}}.mail-detail-content>div[id*=ox-]>h1,.mail-detail-content>div[id*=ox-]>h2,.mail-detail-content>div[id*=ox-]>h3,.mail-detail-content>div[id*=ox-]>h4,.mail-detail-content>div[id*=ox-]>h5{{margin-top:0}}</style>
                        <style>.mail-detail-content .alertHeader {{ text-align: center; line-height: 30px; font-size: 16px; color: rgb(51, 51, 51); font-weight: bold; width: 100%; }} .mail-detail-content .ControlAlert {{ background-color: rgb(173, 216, 230); }} .mail-detail-content .internalControlAlert {{ background-color: rgb(156, 207, 0); }} .mail-detail-content .auditImplication {{ background-color: rgb(0, 112, 192); }} .mail-detail-content .action {{ background-color: rgb(49, 154, 99); }} .mail-detail-content .additional_info {{ background-color: rgb(153, 109, 144); }} .mail-detail-content .alertLabel {{ line-height: 20px; font-size: 12px; color: rgb(51, 51, 51); font-weight: bold; width: 150px; }} .mail-detail-content .alertValue {{ line-height: 20px; font-size: 12px; color: black; width: 100%; }} .mail-detail-content .cell {{ border: 1px solid black; width: 30%; padding: 5px; text-align: left; }} </style>
            
                        </head>
                        <body class="mail-detail-content noI18n colorQuoted">
            
            
            
                            <table cellspacing="0" cellpadding="0" border="0" width="70%" style="margin:0 auto; margin-top:2rem">
                                <tbody>
                                <tr>
                                <td colspan="2" class="alertHeader internalControlAlert">OBSERVATION
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre style="margin-bottom: 1rem;">{1}</pre>
                                                        
                            </td></tr>
                            <tr>
                                <td colspan="2" class="alertHeader auditImplication">IMPLICATION
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre class="alertValue" style="margin-bottom: 1rem;">{8} </pre>
                                </td><td>
                            </td></tr>
                            <tr>
                                <td colspan="2" class="alertHeader action">ACTION
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre class="alertValue" style="margin-bottom: 1rem;">{9}</pre>
                                </td><td>
                        </td></tr>
                        
                    <tr>
                                <td colspan="2" class="alertHeader action">CONTROL PROCESS
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre class="alertValue" style="margin-bottom: 1rem;">{4}</pre>
                                </td><td>
                        </td></tr>
                                
                                <tr>
                                    <td colspan="2" class="alertHeader internalControlAlert" style="align:left;">MANUAL EXCEPTION DETALS
                                </td></tr>
                            
                            
                
                            
                             <tr>
                                <td class="cell">Branch Code</td>
                                <td class="cell">{2}</td>
                            </tr>
                             <tr>
                                <td class="cell">Severity Level</td>
                                <td class="cell">{3}</td>
                            </tr>

                             <tr>
                                <td class="cell">Review Date</td>
                                <td class="cell">{5}</td>
                            </tr>

                             <tr>
                                <td class="cell">Exception Owner</td>
                                <td class="cell">{6}</td>
                            </tr>
                                    <tr>
                                <td class="cell">Inputter</td>
                                <td class="cell">{7}</td>
                            </tr>
                        
                            </tbody></table>
                                <a href="http://127.0.0.1:8000/manual_exception/indexfrommail/{0}">Click here to Review  </a>

                            </body></html>        """.format(exceptionid, exceptiontitle, branchcode, severitylevel, controlprocess, reviewdate, exceptionowner, inputter, implication, action)

            sender_email = "adegokeadeleke.ayo@gmail.com"
            rcp = recipientemail
            x = recipientemail.split(',')

            # b_c=str(x)[1:-1]

            password = "alvvcakmxqbfgvfa"
            message = MIMEMultipart("alternative")
            message["Subject"] = "Manual Exception "+str(exceptionid)
            message["From"] = request.session["username"]
            message["To"] = ','.join([rcp])

            part2 = MIMEText(a, "html")
            if ('fp' in request.FILES):
                myfile = request.FILES['fp']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                uploaded_file_url = fs.url(filename)
                # print(uploaded_file_url,"djffffffffffffffffffffffffffffffffffff")
                request.session['uploaded_file_url'] = uploaded_file_url
                files = "C:/Adroitdeveloments/iconcept4/media/" + \
                    str(request.FILES['fp'])
                with open(files, "rb") as fil:
                    part = MIMEApplication(
                        fil.read(),
                        Name=basename(files)
                    )
                # After the file is closed
                    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(
                        files)
                    message.attach(part)
            message.attach(part2)
            # message.attach(files)
            myid = email.utils.make_msgid()
            # exceptionfilter.CallOver_ID=myid
            message.add_header("In-Reply-To", exceptionid)
            message.add_header("References", exceptionid)
            context = ssl.create_default_context()

            cursor = connection.cursor()
            results = cursor.execute(
                """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailAddress' """)
            # username=cursor.fetchone()
            for result in results:
                username = result[0]
            results = cursor.execute(
                """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailServer' """)
            # username=cursor.fetchone()
            for result in results:
                smtpserver = result[0]
            results = cursor.execute(
                """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailPort' """)
            # username=cursor.fetchone()
            for result in results:
                smtpport = result[0]
            results = cursor.execute(
                """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailUserPassword' """)
            # username=cursor.fetchone()
            for result in results:
                password = result[0]
            to = x

            print(">>>>>>>>>>", to)
            usename = ""
            # usename+=str(username)
            # exceptionfilter.save()
            gmail_user = request.session["username"]
            gmail_pwd = 'Iconcept4nbas'
            smtpserver = smtplib.SMTP("""{0}""".format(
                smtpserver), """{0}""".format(smtpport))
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            # smtpserver.login('adegokeadeleke.ayo@gmail.com',password)
            smtpserver.sendmail(
                request.session['username'], to, message.as_string())

            smtpserver.close()

            print('SUCCESS')

            return HttpResponseRedirect(reverse('indexall'))

    else:
        return HttpResponseRedirect(reverse('login'))


def EditManualException(request):
    request.session.set_expiry(60*25)
    if('userparam' in request.session):

        sdsignal = 'send'

        print(sdsignal)

        if (sdsignal == 'send'):

            cursor1 = connection.cursor()
            exceptionid = request.POST['exceptionid']
            recipientemail = request.POST['recipientemail']
            recipientemail += ',' + request.POST['inputter']

            today = datetime.now()
            stringDate = today.strftime("%m%d%Y,%H:%M:%S")
            prev_comments = request.POST['prevcomments']
            comments = ''
            comments += prev_comments
            comments += '\n' + request.session['userparam']
            comments += ' [' + stringDate + ']: ' + request.POST['comments']
            controlprocess = request.POST['controlprocess']
            action = request.POST['action']
            implication = request.POST['implication']
            branchcode = request.POST['branchcode']
            severitylevel = request.POST['severitylevel']
            reviewdate = request.POST['reviewdate']
            inputter = request.POST['inputter']
            owner = request.POST['owner']
            cursor = connection.cursor()
            cursor.execute('''
                                                UPDATE MANUAL_EXCEPTION
                            SET IC4_REASON = %s ,EXCEPTION_STATUS='REVIEWED'
                            WHERE EXCEPTION_ID = %s
                         ''', (comments, exceptionid))
            cursor.execute(''' COMMIT ''')
            useractivity(request.session.session_key, "Manual Exception", socket.gethostbyname(socket.gethostname()), socket.gethostname(),
                         request.session['username'], today_date, "Sucess", "Click", request.session.session_key, "Manual Exception",
                         """ {0} edited  manual exception with manual exception id {1} """.format(request.session['username'], exceptionid), today, today)

            a = """\
                                                <html lang="en"><head><style>body{{margin:0;padding:0;overflow-x:auto!important;overflow-y:hidden!important}}.mail-detail-content{{box-sizing:border-box;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;font-size:13px;font-weight:400;font-feature-settings:"liga" 0;width:100%;position:relative;padding:0}}.ios.smartphone .mail-detail-content{{-webkit-overflow-scrolling:touch;overflow-x:auto}}.smartphone .mail-detail-content{{font-size:15px}}.mail-detail-content>div>[class$="-content"]{{padding:0}}.mail-detail-content.plain-text{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;white-space:pre-wrap}}.mail-detail-content.plain-text blockquote{{white-space:normal}}.mail-detail-content.fixed-width-font,.mail-detail-content.fixed-width-font.plain-text,.mail-detail-content.fixed-width-font blockquote,.mail-detail-content.fixed-width-font.plain-text blockquote,.mail-detail-content.fixed-width-font blockquote p,.mail-detail-content.fixed-width-font.plain-text blockquote p{{font-family:monospace;-webkit-font-feature-settings:normal;font-feature-settings:normal}}.mail-detail-content.simple-mail{{max-width:700px}}.mail-detail-content.simple-mail.big-screen{{max-width:100%}}.mail-detail-content.simple-mail img{{max-width:100%;height:auto!important}}.mail-detail-content img[src=""]{{background-color:rgba(0,0,0,.1);background-image:repeating-linear-gradient(45deg,transparent,transparent 20px,rgba(255,255,255,.5) 20px,rgba(255,255,255,.5) 40px)}}.mail-detail-content p{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;margin:0 0 1em}}.mail-detail-content h1{{font-size:28px}}.mail-detail-content h2{{font-size:21px}}.mail-detail-content h3{{font-size:16.38px}}.mail-detail-content h4{{font-size:14px}}.mail-detail-content h5{{font-size:11.62px}}.mail-detail-content h6{{font-size:9.38px}}.mail-detail-content a{{word-break:break-word;text-decoration:none;color:inherit}}.mail-detail-content a:hover{{color:inherit}}.mail-detail-content a[href]{{color:#3c61aa;text-decoration:underline}}.mail-detail-content th{{padding:8px;text-align:center}}.mail-detail-content th[align=left]{{text-align:left}}.mail-detail-content .calendar-detail .label{{display:block;text-shadow:none;font-weight:400;background-color:transparent}}.mail-detail-content img.emoji-softbank{{margin:0 2px}}.mail-detail-content pre{{word-break:keep-all;word-break:initial;white-space:pre-wrap;background-color:transparent;border:0 none;border-radius:0}}.mail-detail-content table{{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif;font-size:13px;font-weight:400;font-feature-settings:"liga" 0;line-height:normal;border-collapse:collapse}}.mail-detail-content ul,.mail-detail-content ol{{padding:0;padding-left:16px;margin:1em 0 1em 24px}}.mail-detail-content ul{{list-style-type:disc}}.mail-detail-content ul ul{{list-style-type:circle}}.mail-detail-content ul ul ul{{list-style-type:square}}.mail-detail-content li{{line-height:normal;margin-bottom:.5em}}.mail-detail-content blockquote{{color:#555;font-size:13px;border-left:2px solid #ddd;padding:0 0 0 16px;margin:16px 0}}.mail-detail-content blockquote p{{font-size:13px}}.mail-detail-content blockquote blockquote{{border-color:#283f73;margin:8px 0}}.mail-detail-content.colorQuoted blockquote blockquote{{color:#283f73!important;border-left:2px solid #283f73}}.mail-detail-content.colorQuoted blockquote blockquote a[href]:not(.deep-link){{color:#283f73}}.mail-detail-content.colorQuoted blockquote blockquote a[href]:not(.deep-link):hover{{color:#1b2a4d}}.mail-detail-content.colorQuoted blockquote blockquote blockquote{{color:#dd0880!important;border-left:2px solid #dd0880}}.mail-detail-content.colorQuoted blockquote blockquote blockquote a[href]:not(.deep-link){{color:#dd0880}}.mail-detail-content.colorQuoted blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#ac0663}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote{{color:#8f09c7!important;border-left:2px solid #8f09c7}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote a[href]:not(.deep-link){{color:#8f09c7}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#6c0796}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote{{color:#767676!important;border-left:2px solid #767676}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote a[href]:not(.deep-link){{color:#767676}}.mail-detail-content.colorQuoted blockquote blockquote blockquote blockquote blockquote a[href]:not(.deep-link):hover{{color:#5d5d5d}}.mail-detail-content.disable-links a[href]{{color:#aaa!important;text-decoration:line-through!important;cursor:default!important;pointer-events:none!important}}.mail-detail-content .blockquote-toggle{{color:#767676;font-size:13px;padding-left:56px;margin:16px 0;min-height:16px;word-break:break-word}}.mail-detail-content .blockquote-toggle button.bqt{{color:#696969;background-color:#eee;padding:1px 10px;display:inline-block;font-size:14px;line-height:16px;cursor:pointer;outline:0;position:absolute;left:0;border:0}}.mail-detail-content .blockquote-toggle button.bqt:hover,.mail-detail-content .blockquote-toggle button.bqt:focus{{color:#fff;background-color:#3c61aa;text-decoration:none}}.mail-detail-content .max-size-warning{{color:#767676;padding:16px 16px 0;border-top:1px solid #ddd}}.mail-detail-content a.deep-link{{color:#fff;background-color:#3c61aa;text-decoration:none;font-size:90%;font-weight:700;font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue","Segoe UI",Arial,sans-serif!important;padding:.1em 8px;border-radius:3px}}.mail-detail-content a.deep-link:hover,.mail-detail-content a.deep-link:focus,.mail-detail-content a.deep-link:active{{color:#fff;background-color:#2f4b84}}@media print{{.mail-detail-content .collapsed-blockquote{{display:block!important}}.mail-detail-content .blockquote-toggle{{display:none!important}}.mail-detail-content>div[id*=ox-]>h1,.mail-detail-content>div[id*=ox-]>h2,.mail-detail-content>div[id*=ox-]>h3,.mail-detail-content>div[id*=ox-]>h4,.mail-detail-content>div[id*=ox-]>h5{{margin-top:0}}</style>
                        <style>.mail-detail-content .alertHeader {{ text-align: center; line-height: 30px; font-size: 16px; color: rgb(51, 51, 51); font-weight: bold; width: 100%; }} .mail-detail-content .ControlAlert {{ background-color: rgb(173, 216, 230); }} .mail-detail-content .internalControlAlert {{ background-color: rgb(156, 207, 0); }} .mail-detail-content .auditImplication {{ background-color: rgb(0, 112, 192); }} .mail-detail-content .action {{ background-color: rgb(49, 154, 99); }} .mail-detail-content .additional_info {{ background-color: rgb(153, 109, 144); }} .mail-detail-content .alertLabel {{ line-height: 20px; font-size: 12px; color: rgb(51, 51, 51); font-weight: bold; width: 150px; }} .mail-detail-content .alertValue {{ line-height: 20px; font-size: 12px; color: black; width: 100%; }} .mail-detail-content .cell {{ border: 1px solid black; width: 30%; padding: 5px; text-align: left; }} </style>
            
                        </head>
                        <body class="mail-detail-content noI18n colorQuoted">
            
            
            
                            <table cellspacing="0" cellpadding="0" border="0" width="70%" style="margin:0 auto; margin-top:2rem">
                                <tbody>
                                <tr>
                                <td colspan="2" class="alertHeader internalControlAlert">OBSERVATION
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre style="margin-bottom: 1rem;">{1}</pre>
                                                        
                            </td></tr>
                            <tr>
                                <td colspan="2" class="alertHeader auditImplication">IMPLICATION
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre class="alertValue" style="margin-bottom: 1rem;">{8} </pre>
                                </td><td>
                            </td></tr>
                            <tr>
                                <td colspan="2" class="alertHeader action">ACTION
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre class="alertValue" style="margin-bottom: 1rem;">{9}</pre>
                                </td><td>
                        </td></tr>
                        
                    <tr>
                                <td colspan="2" class="alertHeader action">CONTROL PROCESS
                            </td></tr>
                            <tr>
                                <td colspan="2"><pre class="alertValue" style="margin-bottom: 1rem;">{4}</pre>
                                </td><td>
                        </td></tr>
                                
                                <tr>
                                    <td colspan="2" class="alertHeader internalControlAlert" style="align:left;">MANUAL EXCEPTION DETALS
                                </td></tr>
                            
                            
                
                            
                             <tr>
                                <td class="cell">Branch Code</td>
                                <td class="cell">{2}</td>
                            </tr>
                             <tr>
                                <td class="cell">Severity Level</td>
                                <td class="cell">{3}</td>
                            </tr>

                             <tr>
                                <td class="cell">Review Date</td>
                                <td class="cell">{5}</td>
                            </tr>

                             <tr>
                                <td class="cell">Exception Owner</td>
                                <td class="cell">{6}</td>
                            </tr>
                                    <tr>
                                <td class="cell">Inputter</td>
                                <td class="cell">{7}</td>
                            </tr>
                        
                            </tbody></table>
                                <a href="http://127.0.0.1:8000/manual_exception/indexfrommail/{0}">Click here to Review  </a>

                            </body></html>        """.format(exceptionid, comments, branchcode, severitylevel, controlprocess, reviewdate, owner, inputter, implication, action)

            sender_email = "adegokeadeleke.ayo@gmail.com"
            rcp = recipientemail
            x = recipientemail.split(',')

            # b_c=str(x)[1:-1]

            password = "alvvcakmxqbfgvfa"
            message = MIMEMultipart("alternative")
            message["Subject"] = "Manual Exception "+str(exceptionid)
            message["From"] = request.session["username"]
            message["To"] = ','.join([rcp])

            # socks.setdefaultproxy(socks.SOCKS5, 'proxy.', 8080)
            # socks.wra+pmodule(smtplib)
            part2 = MIMEText(a, "html")
            message.attach(part2)
            # message.attach(files)
            myid = email.utils.make_msgid()
            # exceptionfilter.CallOver_ID=myid
            message.add_header("In-Reply-To", exceptionid)
            message.add_header("References", exceptionid)
            # Create secure connection with server and send email
            context = ssl.create_default_context()

            cursor = connection.cursor()
            results = cursor.execute(
                """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailAddress' """)
            # username=cursor.fetchone()
            for result in results:
                username = result[0]
            results = cursor.execute(
                """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailServer' """)
            # username=cursor.fetchone()
            for result in results:
                smtpserver = result[0]
            results = cursor.execute(
                """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailPort' """)
            # username=cursor.fetchone()
            for result in results:
                smtpport = result[0]
            results = cursor.execute(
                """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME = 'SystemMailUserPassword' """)
            # username=cursor.fetchone()
            for result in results:
                password = result[0]
            to = x
            # 'ayodeji.ajimisinmi@wemabank.com'
            print(">>>>>>>>>>", to)
            usename = ""
            # usename+=str(username)
            # exceptionfilter.save()
            gmail_user = request.session["username"]
            gmail_pwd = 'Iconcept4nbas'
            smtpserver = smtplib.SMTP("""{0}""".format(
                smtpserver), """{0}""".format(smtpport))
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.ehlo
            # smtpserver.login('adegokeadeleke.ayo@gmail.com',password)
            smtpserver.sendmail(
                request.session['username'], to, message.as_string())

            smtpserver.close()

            print('SUCCESS')

            return HttpResponseRedirect(reverse('manualexception'))

    else:
        return HttpResponseRedirect(reverse('login'))


@csrf_exempt
def Observation(request):
    print("Getting other details from description mex.....")

    Selected = request.POST['selected']
    request.session['selected'] = Selected
    # query_result = __get_ob_result(Selected)
    query = ''' SELECT * FROM MANUAL_OBSERVATION WHERE DESCRIPTION= '{0}' '''.format(
        Selected)
    cursor = connection.cursor()
    results = dictfetchall(cursor.execute(query))
    print(results)
    for result in results:
        # print(result['SEVERITY_LEVEL']+"severrrrrrrrrrrrrr")
        implication = str(result['IMPLICATION'])
        severitylevel = str(result['SEVERITY_LEVEL'])
        action = str(result['ACTION'])
    args = {
        'implication': (implication),
        'action': (action),
        'severitylevel': severitylevel

    }
    print(args)

    return JsonResponse(args)
