from io import BytesIO


import requests
import time

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q



from .models import *
from .forms import BookCreate,EmpCreate
# from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd
from iconcept4.models import IC4_Callover
from .queries import *
from django.db import connection
from django.urls import reverse
from .services.ldap import get_LDAP_user
from userapp.models import Roless
import ldap3
from laurelin.ldap import LDAP
import random
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.utils
import socket
from datetime import datetime
today=datetime.date(datetime.now())
date_time=datetime.now()
import os




def useractivity(sessionid,threadid,computerip,computername,userid,creatordate,logtype,logtext,pluginid,ic4application,
                    ic4operation,ic4recorddate,ic4recorddatetime):
    print("transactionid..............",sessionid)
    # query = """
    #          INSERT INTO IC4_PRO_EVENTS_LOG
    #                         ( SESSION_ID,THREAD_ID,COMPUTER_IP,COMPUTER_NAME,USER_ID,CREATOR_DATE,LOG_TYPE,LOG_TEXT,PLUGIN_ID,
    #                         IC4_APPLICATION,IC4_OPERATION,IC4_RECORD_DATE,IC4_RECORD_DATETIME)
    #                         VALUES
    #                         (
    #                         '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '30-APR-15', '{8}', 
    #                         '{9}', '{10}', '{11}', '{12}'
    #                     )
    #         """.format(sessionid,threadid,computerip,computername,userid,creatordate,logtype,logtext,pluginid,ic4application,ic4operation,
    #         ic4recorddate,ic4recorddatetime)
    # cursor = connection.cursor()
    # cursor.execute(query)
    directory = "GeeksforGeeks"


    parent_dir = "D:/"


    path = os.path.join(parent_dir, directory)


    # os.mkdir(path)
    # print("Directory '% s' created" % directory)


    directory = "Geeks"

    parent_dir = "D:/GeeksforGeeks"

    mode = 0o666


    # path = os.path.join(parent_dir, directory)
    tday=datetime.today().strftime('%Y-%m-%d')
    dayandt=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
    getitdone(userid)
    try:
        # os.mkdir(path, mode)
        f= open("C:\IC4LOGS\IC4-2021-07-04\{0}-{1}.txt".format(userid,tday),"a+")
        
            
        f.write("""{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|{8}|{9}|{10}|{11}|{12}""".format(sessionid,threadid,computerip,computername,userid,tday,logtype,logtext,pluginid,ic4application,ic4operation,ic4recorddate,dayandt)   +"\r\n" )
            
    except OSError as error:
        print(error)
    else:
        print("Directory '% s' created" % directory)
        



def getitdone(userid):
    print("i was here")
    tday=datetime.today().strftime('%Y-%m-%d')
    try:
        f= open("C:\IC4LOGS\IC4-2021-07-04\{0}-{1}.txt".format(userid,tday),"r")
    except OSError as error:
        f= open("C:\IC4LOGS\IC4-2021-07-04\{0}-{1}.txt".format(userid,tday),"a+")
        f.write("""session Id|trehad|computer ip|computername|userid|creatordate|logtype|logtext|pluginid|ic4application|ic4operation|ic4recorddate|ic4recorddatetime"""+"\r\n")
        f.close()
    else:
        f.close()
        print("Yes")
    
def togobacktologin(request):
    return(HttpResponseRedirect(reverse('login')))

branch_cd="0"
@csrf_exempt
def indexoflogin(request):
    if(request.POST.get('username')):
        username=request.POST.get('username')
        password=request.POST.get('password')
        
 
        query_result = __get_ldap_setting()
        query_url = __get_ldapurl()
        query_domain = __get_ldapdomain()
        query_dn = __get_ldapdn()
        LDAP_SERVER=""
        uid = False
             
        LdapAuthentication = query_result['LdapAuthentication']
        LdapConnectionUrl = query_url['LdapConnectionUrl']
        LdapAuthenticationDomain = query_domain['LdapAuthenticationDomain'] 
        LdapUserDn = query_dn['LdapUserDn']
        print('LdapAuthentication:',LdapAuthentication)
        print('LdapConnectionUrl:',LdapConnectionUrl)
        print('LdapAuthenticationDomain:',LdapAuthenticationDomain)
        print('LdapUserDn:',LdapUserDn)
        LdapAuthentication=str(LdapAuthentication)
        LdapConnectionUrl=str(LdapConnectionUrl)
        LdapAuthenticationDomain=str(LdapAuthenticationDomain)
        LdapUserDn=str(LdapUserDn)
        if LdapAuthentication.upper()=='YES':
            print('AD enabled')
            ldhost=''' SELECT TO_CHAR('@'||CONF_VALUE) CONF_VALUE FROM U_IC4INDEP.IC4_CORE_CONFIGURATIONS
                                        WHERE NAME = 'LdapAuthenticationDomain' '''
            cursor_ldhost=connection.cursor()
            ldhostres=dictfetchall(cursor_ldhost.execute(ldhost))
            for index in range(len(ldhostres)):
                
                for key in ldhostres[index]:
                    ldhost_res=ldhostres[index][key]

            # print(">>>>>resulturllllllllll",resurl)
            
            username+=ldhost_res
            ldapusername=request.POST.get('username')
            ldhost=''' SELECT TO_CHAR('@'||CONF_VALUE) CONF_VALUE FROM U_IC4INDEP.IC4_CORE_CONFIGURATIONS
                                WHERE NAME = 'BankUsersDomain' '''
            cursor_ldhost=connection.cursor()
            ldhostres=dictfetchall(cursor_ldhost.execute(ldhost))
            for index in range(len(ldhostres)):
                
                for key in ldhostres[index]:
                    ldhost_res=ldhostres[index][key]

            # print(">>>>>resulturllllllllll",resurl)
            
            
            
            # username+="@asoplc.local"
            # ldapusername=request.POST.get('username')
            ldapusername+=ldhost_res
            print("ldap   usernameeeeeeee",ldapusername)
            print("normal   usernameeeeeeee",username)
            # ldapusername+="@asoplc.local"
            a=""
            query_url=''' SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME='calloverurl' '''
            cursor_calloverurl=connection.cursor()
            urlres=dictfetchall(cursor_calloverurl.execute("""  SELECT CONF_TYPE FROM IC4_CORE_CONFIGURATIONS WHERE NAME='calloverurl' """))
            for index in range(len(urlres)):
                
                for key in urlres[index]:
                    resurl=urlres[index][key]

            print(">>>>>resulturllllllllll",resurl)
            request.session['calloverurl']=resurl
            # print("userrr::::",username)
            try:
                if('password' in request.session):

                    if(request.session["userparam"]==username and request.session["password"]==password):
                        request.session["username"]=ldapusername
                        # query3 = '''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(ldapusername)
                        # query_ldapuserId='''SELECT LDAP_USER_ID FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(ldapusername)
                        cursor_ldapuserId=connection.cursor()
                        cursor_ldapuserId.execute('''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID=%(ldapusername)s  ''',{'ldapusername':ldapusername})
                        ldaplist=dictfetchall(cursor_ldapuserId)

                        request.session['ldapId']=username

                        cursor3=connection.cursor()
                        cursor3.execute('''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID=%(ldapusername)s  ''',{'ldapusername':ldapusername})
                        yList3 = dictfetchall(cursor3)
                        branch=''
                        for index in range(len(yList3)):
                            for key in yList3[index]:
                                branch=yList3[index][key]
                                print(branch)
                        request.session['secondarybranch'] =branch

                        request.session['profile']=''
                        useractivity(request.session.session_key,"threadid",socket.gethostbyname(socket.gethostname()),socket.gethostname(),request.session['username'],
                                today_date,"Sucess","Authenticated",request.session.session_key,"iConcept4",
                                    "User Logged In",today,today_date)
                        return HttpResponseRedirect(reverse('index'))
                else:
                    
                    with LDAP()  as ldap:
                        
                        user=""
                        if('password' in request.session):
                            if(request.session["userparam"]==username and request.session["password"]==password):
                                request.session["username"]=ldapusername
                                # query3 = '''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(ldapusername)
                                query_ldapuserId='''SELECT LDAP_USER_ID FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(ldapusername)
                                cursor_ldapuserId=connection.cursor()

                                cursor_ldapuserId.execute('''SELECT LDAP_USER_ID FROM IC4_PRO_USERS WHERE USER_ID=%(ldapusername)s  ''',{'ldapusername':ldapusername})
                                ldaplist=dictfetchall(cursor_ldapuserId)
                                
                                request.session['ldapId']=username

                                cursor3=connection.cursor()
                                cursor3.execute('''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID=%(ldapusername)s  ''',{'ldapusername',ldapusername})
                                yList3 = dictfetchall(cursor3)
                                branch=''
                                for index in range(len(yList3)):
                                    for key in yList3[index]:
                                        branch=yList3[index][key]
                                        print(branch)
                                request.session['secondarybranch'] =branch

                                request.session['profile']=''
                                useractivity(request.session.session_key,"threadid",socket.gethostbyname(socket.gethostname()),socket.gethostname(),request.session['username'],
                                    today_date,"Sucess","Authenticated",request.session.session_key,"iConcept4",
                                        "User Logged In",today,today_date)
                                return HttpResponseRedirect(reverse('index'))
                        else:
                        
                            try:
                                user=ldap.simple_bind(username=username,password=password)
                            
            
                                print("Error message")
                            except:
                                try:
                                    user=ldap.simple_bind(username=username,password=password)
                                    print("Error")
                                except Exception as e:
                                    # if(e=="Got ResultCode('invalidCredentials') for bindResponse (ID 3) (80090308: LdapErr: DSID-0C09044E, comment: AcceptSecurityContext error, data 52e, v2580)"):
                                    #     request.session["userparam"]=username
                                    #     request.session["password"]=password
                                    # request.session['profile']=''    
                                    # return HttpResponseRedirect(reverse('index'))
                                    # else:
                                    useractivity(request.session.session_key,"threadid",socket.gethostbyname(socket.gethostname()),
                                            socket.gethostname(),request.session['username'],
                                            today_date,"Failed","Blocked",request.session.session_key,"iConcept4",
                                                "Login Failed",today,today_date)
                                    
                                    return render(request, 'allauth/account/login.html',{"error":e})
                                    # return render(request, 'allauth/account/login.html', {"error": e})
                                # print('Returned User',user)
                                else:
                                    request.session["username"]=ldapusername.replace('.local','.com')
                                    request.session["userparam"]=username
                                    request.session["password"]=password
                                    query3 = '''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(ldapusername)
                                    # query_ldapuserId='''SELECT LDAP_USER_ID FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(ldapusername)
                                    cursor_ldapuserId=connection.cursor()
                                    cursor_ldapuserId.execute('''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID=%(ldapusername)s  ''',{'ldapusername':ldapusername})
                                    ldaplist=dictfetchall(cursor_ldapuserId)
                                   
                                    request.session['ldapId']=ldapusername

                                    cursor3=connection.cursor()
                                    cursor3.execute('''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID=%(ldapusername)s  ''',{'ldapusername':ldapusername})
                                    yList3 = dictfetchall(cursor3)
                                    branch=''
                                    for index in range(len(yList3)):
                                        for key in yList3[index]:
                                            branch=yList3[index][key]
                                            print(branch)
                                    request.session['secondarybranch'] =branch

                                    request.session['profile']=''
                                    useractivity(request.session.session_key,"threadid",socket.gethostbyname(socket.gethostname()),socket.gethostname(),request.session['username'],
                                    today_date,"Sucess","Authenticated",request.session.session_key,"iConcept4",
                                        "User Logged In",today,today_date)
                                    return HttpResponseRedirect(reverse('index'))
                                    
                                
                                
                            else:
                                request.session["username"]=ldapusername.replace('.local','.com')
                                request.session["userparam"]=username
                                request.session["password"]=password   
                                # query3 = '''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(ldapusername)
                                # query_ldapuserId='''SELECT LDAP_USER_ID FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(ldapusername)
                                cursor_ldapuserId=connection.cursor()
                                cursor_ldapuserId.execute('''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID=%(ldapusername)s  ''',{'ldapusername':ldapusername})
                                ldaplist=dictfetchall(cursor_ldapuserId)
                                
                                request.session['ldapId']=username

                                cursor3=connection.cursor()
                                cursor3.execute('''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID=%(ldapusername)s  ''',{'ldapusername':ldapusername})
                                yList3 = dictfetchall(cursor3)
                                branch=''
                                for index in range(len(yList3)):
                                    for key in yList3[index]:
                                        branch=yList3[index][key]
                                        print(branch)
                                request.session['secondarybranch'] =branch

                                request.session['profile']=''
                                useractivity(request.session.session_key,"threadid",socket.gethostbyname(socket.gethostname()),socket.gethostname(),request.session['username'],
                                    today_date,"Sucess","Authenticated",request.session.session_key,"iConcept4",
                                        "User Logged In",today,today_date)
                                return HttpResponseRedirect(reverse('index'))
                
            except Exception as e:
                # if(e=="Got ResultCode('invalidCredentials') for bindResponse (ID 3) (80090308: LdapErr: DSID-0C09044E, comment: AcceptSecurityContext error, data 52e, v2580)"):
                #     request.session["userparam"]=username
                #     request.session["password"]=password
                # request.session['profile']=''    
                # return HttpResponseRedirect(reverse('index'))
                # else:
                useractivity(request.session.session_key,"threadid",socket.gethostbyname(socket.gethostname()),
                socket.gethostname(),request.session['username'],
                today_date,"Failed","Blocked",request.session.session_key,"iConcept4",
                    "Login Failed",today,today_date)
                return render(request, 'allauth/account/login.html',{"error": e})
            else:
                query3 = '''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(ldapusername.replace('.local','.com'))
                # query_ldapuserId='''SELECT LDAP_USER_ID FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(ldapusername.replace('.local','.com'))
                cursor_ldapuserId=connection.cursor()
                cursor_ldapuserId.execute('''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID=%(ldapusername)s  ''',{'ldapusername':ldapusername})
                ldaplist=dictfetchall(cursor_ldapuserId)
                request.session["username"]=ldapusername.replace('.local','.com')
                request.session['ldapId']=username

                cursor3=connection.cursor()
                cursor3.execute('''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID=%(ldapusername)s  ''',{'ldapusername':ldapusername})
                yList3 = dictfetchall(cursor3)
                branch=''
                for index in range(len(yList3)):
                    for key in yList3[index]:
                        branch=yList3[index][key]
                        print(branch)
                request.session['secondarybranch'] =branch

                request.session["userparam"]=username
                request.session["password"]=password
                request.session['profile']=''
                useractivity(request.session.session_key,"threadid",socket.gethostbyname(socket.gethostname()),socket.gethostname(),request.session['username'],
                                    today_date,"Sucess","Authenticated",request.session.session_key,"iConcept4",
                                        "User Logged In",today,today_date)
                return HttpResponseRedirect(reverse('index'))
                             
        else:
            
            cursor_calloverurl=connection.cursor()
            urlres=dictfetchall(cursor_calloverurl.execute("""  SELECT CONF_TYPE FROM IC4_CORE_CONFIGURATIONS WHERE NAME='calloverurl' """))
            for index in range(len(urlres)):
                
                for key in urlres[index]:
                    resurl=urlres[index][key]

            print(">>>>>resulturllllllllll",resurl)
            request.session['calloverurl']=resurl
            cursor = connection.cursor()
        
            cursor.execute(""" SELECT *  FROM IC4_PRO_USERS  where USER_ID=%s and USER_PWD=%s  """,(username,password))
            yList = dictfetchall(cursor)
    
            if yList:
                # print(yList)

                global branch_cd
                branch_cd="010"
                # branch=yList.BRANCH_CODE
                # print(yList)
                request.session['userparam'] = request.POST.get('username')
                request.session["username"]=request.POST.get('username')
                # query3 = '''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(username)
                # query_ldapuserId='''SELECT LDAP_USER_ID FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(username)
                cursor_ldapuserId=connection.cursor()
                cursor_ldapuserId.execute('''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID=%(ldapusername)s  ''',{'ldapusername':username})
                ldaplist=dictfetchall(cursor_ldapuserId)
                for index in range(len(ldaplist)):
                    for key in ldaplist[index]:
                        ldapId=ldaplist[index][key]
                        print(ldapId)
                request.session['ldapId']=ldapId

                cursor3=connection.cursor()
                cursor3.execute('''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID=%(username)s  ''',{'username':username})
                yList3 = dictfetchall(cursor3)
                branch=''
                for index in range(len(yList3)):
                    for key in yList3[index]:
                        branch=yList3[index][key]
                        print(branch)
                request.session['secondarybranch'] =branch
                request.session['profile']=''
                useractivity(request.session.session_key,"threadid",socket.gethostbyname(socket.gethostname()),socket.gethostname(),request.session['username'],
                                    today_date,"Sucess","Authenticated",request.session.session_key,"iConcept4",
                                        "User Logged In",today,today_date)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, 'allauth/account/login.html', {"error": "username or password incorrect"})
    return render(request, 'allauth/account/login.html', {"": ""})


def returnallbranch(secondarybranch,username):
    query2 = '''SELECT BRANCH_CODE FROM USER_BRANCHES WHERE USER_ID='{0}'  '''.format(username)
    cursor2=connection.cursor()
    result2=cursor2.execute('''SELECT BRANCH_CODE FROM USER_BRANCHES WHERE USER_ID=%(username)s  ''',{'username':username})
    yList2=dictfetchall(cursor2)
    # print(yList2)
    b_c=''
    for index in range(len(yList2)):
        for key in yList2[index]:
            b_c+=yList2[index][key]+","
        
            # print(yList2[index][key])
            # print(b_c)
    b_c+=secondarybranch
    x = b_c.split(',')

    b_c=str(x)[1:-1]
    return b_c

def index(request):
    request.session.set_expiry(60*25)
    if('userparam' in request.session):
        request.session.set_expiry(60*25)
        cursor_alienuserid=connection.cursor()
       
        
        cursor_alienuserid.execute("""  SELECT LDAP_USER_ID FROM U_IC4INDEP.IC4_PRO_USERS
            WHERE USER_ID = %(username)s  """,{'username':request.session['username']})
    

        
        
        alienid=dictfetchall(cursor_alienuserid)
        for index in range(len(alienid)):
            for key in alienid[index]:
                rest=alienid[index][key]
                b=''
              
        request.session['alienid']=rest
   

        b_c = ''
        print(request.session['username'])
        username=request.session['username']
        today_date = '19-JUL-18'
        
        
        b_c=returnallbranch(request.session['secondarybranch'],request.session['username'])
        print(b_c)
        
       
        request.session['allbranches']=b_c
        # print(b_c)
        transLimit=''
        if (request.POST.get('transLimit') is not None):
            transLimit=int(request.POST.get('transLimit'))
        request.session['transLimit']=0
    
        if (transLimit is not  None):
            if type(transLimit) == int or type(transLimit) == float:
                request.session['transLimit']=transLimit
            else:
                request.session['transLimit']=0
        print("transaction limmmmmmm",request.session['transLimit'])
        cursor = connection.cursor()
        useractivity(request.session.session_key,"Callover for Tellers",socket.gethostbyname(socket.gethostname()),socket.gethostname(),request.session['username'],
                                    today_date,"""{0} visited the first summary page""".format(request.session['username']),"Callover for Tellers",request.session.session_key,"U-review",
                                        "Callover",today,today_date)
        request.session['profile']="Select Profile"
        if (request.POST.get('profile')):
            useractivity(request.session.session_key,"Callover for Tellers",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
            request.session['username'],
            today_date,"""{0} visited the first summary page and grouped by profile {1}""".format(request.session['username'],
            request.POST.get('profile')),"Callover for Tellers",request.session.session_key,"U-review",
            "Callover",today,today_date)

            request.session['profile']=request.POST.get('profile')
            
        else:
            print("b_cccccccccccccccccccc",b_c)
            tuple11=(b_c,request.session['username'],request.session['transLimit'])
            cursor.execute("""SELECT IC4_BRANCH_CODE, GRP_BY_DATE, SUM(CALL_NO_OF_VOUCHERS) as NO_OF_ENTRIES, 
            SUM(CALL_CREDIT_FREQ) as NO_OF_CREDIT, SUM(CALL_DEBIT_FREQ) as NO_OF_DEBIT, TO_CHAR(SUM(CALL_CREDIT_TOTAL), 
            'FM99,999,999,999,999.00') as CREDIT_TOTAL_CALL, TO_CHAR(SUM(CALL_DEBIT_TOTAL), 'FM99,999,999,999,999.00') as 
            DEBIT_TOTAL_CALL FROM ( SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM 
            ( SELECT IC4_BRANCH_CODE, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as 
            CALL_NO_OF_VOUCHERS, SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, SUM(CREDIT) CALL_CREDIT_TOTAL, SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, 
            SUM(ABS(DEBIT)) as CALL_DEBIT_TOTAL, SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE 
            FROM ( 	SELECT "TRANS_ID" GRP_BY_REF, "BRANCH_CODE" IC4_BRANCH_CODE, "ENTRY_DATE" GRP_BY_DATE, "IC4_INPUTTER" GRP_BY_USER, 
            CALLOVER_OFFICER, case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ, case when "AMT_FIELD_1" <0 then 1 else 0 end 
            as DEBIT_FREQ, case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT, case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" 
            else 0 end as DEBIT from ( SELECT DISTINCT trans_id, TRANS_REF_ID, TRANS_REF_ID AS REF_ID, TRANS_SUB_ID AS AC_ENTRY_SR_NO, T.BRANCH_CODE,
             BRANCH_NAME, ACCOUNT_ID AS ACCOUNT_NUMBER, ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME , LCY_CODE, FCY_AMOUNT AMT_1, FCY_CODE, TRANS_CODE  AS 
             TXN_C, TRANS_MODE as TRN_REF_NO, CHEQUE_NO, NARRATIVE AS TRANSACTION_NARRATIVE, ENTRY_DATE AS VALUE_DATE, TRAN_DATE, BOOKING_DATE, POSTING_DATE,
              ENTRY_DATE, ENTRY_TIME, IC4_ACCOUNT_OFFICER, T.IC4_INPUTTER , IC4_AUTHORISER , IC4_VERIFIER  , CHECKER_ID, MAKER_ID, TEXT_FIELD_1  ,
               TEXT_FIELD_2, AMT_FIELD_1, to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT, to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,
                AMT_FIELD_2, DATE_FIELD_1, DATE_FIELD_2 , CALLOVER_REMARK, EXCEPTION_ID, SEVERITY_ID, REVIEW_DATE, CALLOVER_OFFICER, T.CALLOVER_DATE, CALLOVER_TIME, 
                IC4_SPECIAL, CHECKER_DATE_TIME, CALLOVER_ID, POST_BRN, BATCH_NO, V_NUM, DOC_NO, DR_TXN_NGN, RATE, TXN_MNEM AS MNEM, AC_GL_BRN_NAME, COD_BANK, 
                TXN_MNEMONIC, TXN_BRANCH, AMOUNT, TIME_KEY, REF_NUM, P.USER_ID FROM CALLOVER_TRANSACTION T, CALLOVER_OP_ASSIGNMENT P WHERE T.BRANCH_CODE IN ( {0} )
                 AND T.IC4_INPUTTER = P.OPERATOR_ID AND TO_CHAR(T.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(P.CALLOVER_DATE, 'YYYY-MM-DD') AND T.BRANCH_CODE = P.BRANCH_CODE 
                 AND T.TXN_MNEMONIC = 'NORMAL' AND P.USER_ID= '{1}' AND T.CALLOVER_OFFICER IS NULL AND EXISTS 
                 ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION B WHERE  B.BRANCH_CODE = T.BRANCH_CODE AND
                  TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(T.ENTRY_DATE, 'YYYY-MM-DD') AND 
                  B.TRANS_ID = T.TRANS_ID AND ABS(B.AMT_FIELD_1) >= {2} AND B.CALLOVER_OFFICER IS NULL ) AND  
                  ACCOUNT_NAME not like 'TILL-INTER' ) a  ) a GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a,
                   PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) ) GROUP BY GRP_BY_DATE, IC4_BRANCH_CODE ORDER BY GRP_BY_DATE, IC4_BRANCH_CODE """.format(b_c,request.session['alienid'],request.session['transLimit']))
        yList = dictfetchall(cursor)
    
        columns = [col[0] for col in cursor.description]
        cursor_profile=connection.cursor()
        profileresult=cursor_profile.execute(''' SELECT DISTINCT B.*, coalesce(P.USER_NAME,B.IC4_INPUTTER) PROFILE_NAME FROM (SELECT DISTINCT T.BRANCH_CODE, T.IC4_INPUTTER, A.USER_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION T, U_IC4INDEP.CALLOVER_OP_ASSIGNMENT A WHERE T.BRANCH_CODE = A.BRANCH_CODE AND T.IC4_INPUTTER = A.OPERATOR_ID AND T.CALLOVER_OFFICER IS NULL ) B LEFT JOIN U_IC4INDEP.PROFILE P ON UPPER(B.IC4_INPUTTER) = UPPER(P.PROFILE_ID) WHERE B.BRANCH_CODE IN (%(branchcode)s) AND USER_ID = %(alienid)s ORDER BY B.BRANCH_CODE, coalesce(P.USER_NAME,B.IC4_INPUTTER) ASC ''',{'branchcode':b_c,'alienid':request.session['alienid']})
        profiles = dictfetchall(profileresult)
        # query3 = '''SELECT GROUP_NAME FROM USERROLE WHERE USER_ID ='{0}'  '''.format(request.session['username'])
        cursor3=connection.cursor()
        cursor3.execute('''SELECT GROUP_NAME FROM USERROLE WHERE USER_ID =%(username)s  ''',{'username':request.session['username']})
        yList3 = dictfetchall(cursor3)
        usergroup=''
        print("ylist333333333",yList3)    # grouplist=''
        for index in range(len(yList3)):
            for key in yList3[index]:
                usergroup=yList3[index][key]
        if (usergroup):
            flag="True"
        else:
            flag="False"
        if (flag=="True"):
            role = Roless.objects.filter(Group_Id=usergroup)
            
            cursor22=connection.cursor()
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Branch Service Tellers' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplist=dictfetchall(cursor22)
            request.session['grouplist']=grouplist                    
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Branch Service BSM/HTS' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplistbsm=dictfetchall(cursor22)
            request.session['grouplistbsm']=grouplistbsm                    
            cursor22=connection.cursor()
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Branch Control' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplistbc=dictfetchall(cursor22)
            request.session['grouplistbc']=grouplistbc                   
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Foreign Operation Tellers' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplistfot=dictfetchall(cursor22)
            request.session['grouplistfot']=grouplistfot
            cursor22=connection.cursor()
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Foreign Operation Control' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplistfoc=dictfetchall(cursor22)
            request.session['grouplistfoc']=grouplistfoc                       
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Treasury Operation Tellers' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplisttrs=dictfetchall(cursor22)
            request.session['grouplisttrs']=grouplisttrs
            
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Treasury Operation Control' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplisttrc=dictfetchall(cursor22)
            request.session['grouplisttrc']=grouplisttrc
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Callover Exception' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplist_ce=dictfetchall(cursor22)
            print("ceeeeeeeeeeeeeeee",grouplist_ce)
            request.session['grouplist_ce']=grouplist_ce  
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Callover Assignment' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplist_ca=dictfetchall(cursor22)
            request.session['grouplist_ca']=grouplist_ca   
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Downgraded Branch' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplist_db=dictfetchall(cursor22)
            request.session['grouplist_db']=grouplist_db 
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Exception Manager' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplist_ei=dictfetchall(cursor22)
            request.session['grouplist_ei']=grouplist_ei                 
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Concurrency' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplistcon=dictfetchall(cursor22)
            request.session['grouplistcon']=grouplistcon
            cursor22.execute('''SELECT * FROM ROLE WHERE MENU_HEAD='Report' AND GROUP_ID_ID =%(usergroup)s  ''',{'usergroup':usergroup})
            grouplistcon=dictfetchall(cursor22)
            request.session['grouplistreport']=grouplistcon            
            return render(request, 'book/library.html', {'prof_session':request.session['profile'],'results':yList, 'transLimit':request.session['transLimit'],'Profiles':profiles, 'test':branch_cd,'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei'],'grouplist_report':request.session['grouplistreport']})
        else:
            request.session['err']="No role is assigned to this user"
            # reverse('alertreviewindex',args=(),kwargs={'id':alertid})
            return render(request, 'allauth/account/login.html', {"error": "No role is assigned to this user"})
    else:
        # useractivity(request.session.session_key,"Callover for Tellers",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        #             request.session['username'],
        #             "today_date","""session timed out on""","Callover for Tellers",request.session.session_key,"U-review",
        #             "Callover",today,"today_date")


        return HttpResponseRedirect(reverse('login'))





def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def testing(request):
    shelf=Book.objects.all()
    return render(request,'book/abc.html',{'shelf':shelf})
# @staff_member_required
def upload(request):
    upload = EmpCreate()
    if request.method == 'POST':
        upload = EmpCreate(request.POST, request.FILES)
        if upload.is_valid():
            upload.save()
            return redirect('index')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
    else:
        return render(request, 'book/upload_form.html', {'upload_form':upload})
# @staff_member_required
def update_book(request, book_id):
    book_id = int(book_id)
    try:
        book_sel = Employee.objects.get(id = book_id)
    except Employee.DoesNotExist:
        return redirect('index')
    book_form = EmpCreate(request.POST or None, instance = book_sel)
    if book_form.is_valid():
       book_form.save()
       return redirect('index')
    return render(request, 'book/upload_form.html', {'upload_form':book_form})

# for deleting multiple profiles
@csrf_exempt #Add this too.
@staff_member_required
def book_Delete(request, id=None):

    if request.method == 'POST': #<- Checking for method type
        id_list = request.POST.getlist('instance')
    #This will submit an array of the value attributes of all the
    #checkboxes that have been checked, that is an array of {{obj.id}}

        # Now all that is left is to iterate over the array fetch the
        #object with the ID and delete it.

        for agent_id in id_list:
            Employee.objects.get(id=agent_id).delete()
    return redirect('index')


# for searching
@staff_member_required
def search(request):
    query = request.GET.get('q','')
    #The empty string handles an empty "request"
    if query:
            queryset = (Q(Entry_User_ID__icontains=query) | Q(id__icontains=query))
            #I assume "text" is a field in your model
            #i.e., text = model.TextField()
            #Use | if searching multiple fields, i.e.,
            #queryset = (Q(text__icontains=query))|(Q(other__icontains=query))
            results = Employee.objects.filter(queryset).distinct()
    else:
       results = []
    return render(request, 'book/library.html', {'results':results, 'query':query})

# @staff_member_required


# @staff_member_required
def Profile_Trans(request, Profile_ID):
    query = trans_query_profiles(Profile_ID)
    cursor = connection.cursor()
    result = cursor.execute(query, None)
    ylist=dictfetchall(cursor)

    return render(request, 'callover/branch_trans.html', {'results': ylist})

# @staff_member_required


import json
from datetime import timedelta
from datetime import date
import numpy as np
@csrf_exempt
def Observation(request):
    
    print("Getting other details from observation model......")
   
    Selected = request.POST['selected']
    useractivity(request.session.session_key,"Callover for Tellers",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
                    request.session['username'],
                    today_date,"""{0} clicked on observation {1} while wanting to raise exception""".format(request.session['username'],
                    Selected),
                    "Callover for Tellers",request.session.session_key,"U-review","Callover",today,today_date)
    request.session['selected'] = Selected
    query_result = __get_ob_result(Selected) 
    severity = query_result['severity']
    implication = query_result['implication']
    action = query_result['action']
    request.session['severity'] = severity
    request.session['implication'] = implication
    request.session['action'] = action
    args = {           
            'query_result': query_result
                    
        }

    return JsonResponse(args)








# @staff_member_required
def delete_book(request, id):
    id = int(id)
    try:
        IC4_trans_obj = IC4_Callover.objects.get(id = id)
        # IC4_trans_obj.delete()
    except IC4_Callover.DoesNotExist:
        return HttpResponse(False)
    return HttpResponse(True)

def __get_ob_result(Selected):
    query = ob_query(Selected)
    cursor = connection.cursor()
    results = cursor.execute(query)
    for result in results:
        severity = result[0]
        implication = result[1]
        action = result[2]
        
    Dict =dict()
    Dict['severity'] = severity
    Dict['implication'] = implication
    Dict['action'] = action
   
    return Dict
from datetime import datetime
today=datetime.date(datetime.now())
date_time=datetime.now()
def __update_callover2(transID, calloverID, severity,reviewDate,branchCode,initialdate,grpbuuser,usrid):
        #    __update_callover(id,  my_id, today, todaye,username,branchCode,initialdate,grpbuuser)
    cursor=connection.cursor()

    cursor.execute(''' 
                UPDATE CALLOVER_TRANSACTION
                    SET CALLOVER_DATE = '{9}', 
                    
                    CALLOVER_ID = '{2}', 
                    CALLOVER_TIME='{8}',
                    CALLOVER_OFFICER = '{7}',
                    SEVERITY_ID = '{1}',
                    EXCEPTION_ID = '{2}'
                    WHERE TRUNC(ENTRY_DATE) = '{3}'
                    AND TRANS_ID = '{4}'
                    AND BRANCH_CODE = '{5}'
                    AND IC4_INPUTTER = '{6}'
                 '''.format(reviewDate,severity,calloverID,initialdate,transID,branchCode,grpbuuser,usrid,date_time,today))
    cursor.execute('''commit''')
    print("did thissssssssssssssssssssssssss")
    # transections = IC4_Callover_L3.objects.filter(Trans_ID=transID)
    # for transection in transections:
    #     transection.Exception_Id = calloverID
    #     transection.Severity_Id = severity
    #     transection.Review_Date = reviewDate
    #     transection.save()

def __get_config_result():
    query = comfig_query()
    print('query:',query)
    cursor = connection.cursor()
    print('query2:',query)
    results = cursor.execute(query)
    print('query3:',query)
    for result in results:
        html_text = result[0]
       
    Dict =dict()
    Dict['html_text'] = html_text
    
    return Dict

def __get_query_result(trasn_id):
    print("transactionid..............",trasn_id)
    query = """

                SELECT IC4_BRANCH_CODE, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, TXN_CODE, 
                SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, 
                SUM(CREDIT) CALL_CREDIT_TOTAL, SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, SUM(ABS(DEBIT)) 
                as CALL_DEBIT_TOTAL, SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE FROM
                ( SELECT "TRANS_ID" GRP_BY_REF, "TXN_CODE" TXN_CODE, "BRANCH_CODE" IC4_BRANCH_CODE,
                "ENTRY_DATE" GRP_BY_DATE, "IC4_INPUTTER" GRP_BY_USER, CALLOVER_OFFICER, case when
                "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ, case when "AMT_FIELD_1" <0 
                then 1 else 0 end as DEBIT_FREQ, case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" 
                else 0 end as CREDIT, case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end 
                as DEBIT from ( SELECT ID, trans_id, TRANS_REF_ID, TRANS_REF_ID AS REF_ID, 
                TRANS_SUB_ID AS AC_ENTRY_SR_NO, BRANCH_CODE, BRANCH_NAME, ACCOUNT_ID AS ACCOUNT_NUMBER, 
                ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME , LCY_CODE, to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,   
                to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT, FCY_CODE, TRANS_CODE  AS TXN_C,
                TRANS_MODE as TRN_REF_NO, CHEQUE_NO, NARRATIVE AS TRANSACTION_NARRATIVE, ENTRY_DATE AS VALUE_DATE,
                TRAN_DATE, BOOKING_DATE, POSTING_DATE, ENTRY_DATE, ENTRY_TIME, IC4_ACCOUNT_OFFICER, IC4_INPUTTER ,
                IC4_AUTHORISER , IC4_VERIFIER  , CHECKER_ID, MAKER_ID, TEXT_FIELD_1  , TEXT_FIELD_2, AMT_FIELD_1,
                AMT_FIELD_2, DATE_FIELD_1, DATE_FIELD_2 , CALLOVER_REMARK, EXCEPTION_ID, SEVERITY_ID, REVIEW_DATE,
                CALLOVER_OFFICER, CALLOVER_DATE, CALLOVER_TIME, IC4_SPECIAL, CHECKER_DATE_TIME, CALLOVER_ID, POST_BRN,
                BATCH_NO, V_NUM, DOC_NO, DR_TXN_NGN, RATE, TXN_MNEM AS MNEM, AC_GL_BRN_NAME, COD_BANK, TXN_MNEMONIC, 
                TXN_BRANCH, AMOUNT, TXN_CODE,TIME_KEY, REF_NUM FROM callover_transaction WHERE  BRANCH_CODE <> '000' 
                AND trans_id = '{0}' AND TXN_MNEMONIC = 'NORMAL' AND ACCOUNT_NAME not like 'TILL-INTER%' ) a )
                a GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, TXN_CODE""".format(trasn_id)
    cursor = connection.cursor()
    results = cursor.execute(query)
    for result in results:
        branch = result[0]
        trans_id = result[1]
        date = result[2]
        officer = result[3]
        user = result[4]
        TXN_CODE = result[5]
        credit_amount = int(result[7])
        debit_amount = int(result[9])
        print(">>>>>>>",TXN_CODE)
    
    Dict =dict()
    Dict['branch'] = branch
    Dict['trans_id'] = trans_id
    Dict['date'] = date
    Dict['date2'] = date.strftime("%Y%m%d")
    Dict['date3'] = date.strftime("%d-%m-%Y")
    Dict['user'] = user
    Dict['credit_amount'] = credit_amount
    Dict['debit_amount'] = debit_amount
    Dict['TXN_CODE'] = TXN_CODE
    return Dict

def __get_ldap_setting():
    query = ldap_query()
    cursor = connection.cursor()
    results = cursor.execute(query)
    for result in results:
        LdapAuthentication = result[0]
    Dict =dict()
    Dict['LdapAuthentication'] = LdapAuthentication 
    return Dict

def __get_ldapurl():
    query = ldap_url()
    cursor = connection.cursor()
    results = cursor.execute(query)
    for result in results:
        LdapConnectionUrl = result[0]  
    Dict =dict()
    Dict['LdapConnectionUrl'] = LdapConnectionUrl
    return Dict

def __get_ldapdomain():
    query = ldap_domain()
    cursor = connection.cursor()
    results = cursor.execute(query)
    for result in results:
        LdapAuthenticationDomain = result[0] 
    Dict =dict()
    Dict['LdapAuthenticationDomain'] = LdapAuthenticationDomain
    return Dict

def __get_ldapdn():
    query = ldap_dn()
    cursor = connection.cursor()
    results = cursor.execute(query)
    for result in results:
        LdapUserDn = result[0] 
    Dict =dict()
    Dict['LdapUserDn'] = LdapUserDn
    return Dict


# def __get_user_group(username):
#     print('username:',username)
#     query =  usergrp_query(username)
#     cursor = connection.cursor()
#     results = cursor.execute(query)
#     for result in results:
#         Group = result[0] 
#     Dict =dict()
#     Dict['Group'] = Group
#     return Dict
        

   


def authenticate(request, username, password, LdapConnectionUrl,LdapAuthenticationDomain,LdapUserDn):
        # Get credentials from the query strings 
        # username = request.GET.get('username')
        # password = request.GET.get('password')

        # Get the user information from the LDAP if he can be authenticated
        if get_LDAP_user(username, password,LdapConnectionUrl,LdapAuthenticationDomain,LdapUserDn) is None:
            return False
        else:
            return True


def update_trans(request):
    if request.is_ajax and request.method == "POST":
        id = request.POST['id']
        transection = IC4_Callover.objects.get(pk=id)


        # transection = IC4_Callover.objects.get(id = id)
        trans_ID = request.POST['trans-ID']
        transection.Trans_ID = trans_ID.strip()
        transection.Branch_Code = request.POST['branch']
        transection.Account_ID = request.POST['acc-number']
        transection.Account_Name = request.POST['acc-name']
        # transection.Value_Date = request.POST['date']
        transection.LCY_Amount = request.POST['amount']
        transection.Narrative = request.POST['narrative']
        transection.Ref_Num = "'VOUCHER'010CHDP182000003" # this line has ref_num hardcoded why? it is not active
        # print(transection.Trans_ID, transection.Branch_Code, transection.Account_ID, transection.Account_Name)
        transection.save()

        # transection.save()


    return HttpResponse(True)

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from base64 import b64decode
from datetime import date

# def __get_query_result(trasn_id):
#     query = custom_query(trasn_id)
#     cursor = connection.cursor()
#     results = cursor.execute(query)
#     for result in results:
#         branch = result[0]
#         trans_id = result[1]
#         date = result[2]
#         officer = result[3]
#         user = result[4]
#         TXN_CODE = result[5]
#         credit_amount = int(result[7])
#         debit_amount = int(result[9])
#         print(">>>>>>>",TXN_CODE)
#     Dict =dict()
#     Dict['branch'] = branch
#     Dict['trans_id'] = trans_id
#     Dict['date'] = date
#     Dict['user'] = user
#     Dict['credit_amount'] = credit_amount
#     Dict['debit_amount'] = debit_amount
#     Dict['TXN_CODE'] = TXN_CODE
#     return Dict

def __update_callover(trans_id,callover_id,date, time, username,branchCode,initialdate,grpbuuser):
    cursor=connection.cursor()
    cursor.execute(''' 
                UPDATE CALLOVER_TRANSACTION
            SET CALLOVER_DATE = '{0}', 
            CALLOVER_TIME = '{1}',
            CALLOVER_ID = '{2}', 
            CALLOVER_OFFICER = '{3}'
            WHERE TRUNC(ENTRY_DATE) = '{4}'
            AND TRANS_ID = '{5}'
            AND BRANCH_CODE = '{6}'
            AND IC4_INPUTTER = '{7}'
                 '''.format(date,time,callover_id,username,initialdate,trans_id,branchCode,grpbuuser))
    cursor.execute('''commit''')


def __get_argument(pdf_type,images):
    pdf_type = pdf_type.upper()
    if (pdf_type == "CDP"):
        img = cash_deposit_slip(images[0])
        img.save('ticket.jpg', 'JPEG')
        return 0
    if (pdf_type == "CQW"):
        img = cheque(images[0])
        img.save('ticket.jpg', 'JPEG')
        return 1
    if (pdf_type == "in_house_cheque"):
        img = In_House_cheque(images[0])
        img.save('ticket.jpg', 'JPEG')
        return 2
    if (pdf_type == "CWD"):
        img = withdraw(images[0])
        img.save('ticket.jpg', 'JPEG')
        return 3
    if (pdf_type == "OATAMAN"):
        img = transfer(images[0])
        img.save('ticket.jpg', 'JPEG')
        return 4
    if (pdf_type == "transfer_form"):
        img = transfer_form(images[0])
        img.save('ticket.jpg', 'JPEG')
        return 5
    if (pdf_type == "neft_transfer"):
        img = NEFT_transfer(images[0])
        img.save('ticket.jpg', 'JPEG')
        return 6

import json
from datetime import timedelta
from datetime import date
import numpy as np
@csrf_exempt
def OCR(request):
    print("=====================================================")
    print(request.POST['status'])
    username=request.session['userparam']
    todayd = datetime.now().date()
    todayc=todayd.strftime("%d-%m-%Y")
    today = datetime.now().date()
    t = time.localtime()
    tomorrow = today + timedelta(days=1)
    tomorrowf=tomorrow.strftime("%d-%m-%Y")
    current_time = time.strftime("%H:%M:%S", t)
    todaye=time.strftime("%Y-%m-%d %H:%M:%S", t)

    addt='000'
    current_tim = time.strftime("%H%M", t)
    current_tim2=current_tim+addt
    flag = False
    id = request.POST['id']
    # pdf = request.POST['pdf']
    voucher = request.POST['voucher']
    status = request.POST['status']

    query_result = __get_query_result(id)
    date_only = query_result['date'].strftime("%d-%m-%Y")
    callover_ID = str(query_result['user']) + str(date_only) + query_result['trans_id']

    # bytes = b64decode(pdf, validate=True)
    # images = convert_from_bytes(bytes)
    # img  = images[0]
    request.session['review'] =tomorrowf


    users = query_result['user']
    results = Profile.objects.filter(Profile_ID=users)
    profileId=''
    inputterEmail=''
    for result in results:
        inputterEmail = result.Email
        profileId=result.Profile_ID
    
    obt={
        'rest':IC4_Observation_Model.objects.all()
        
    }
    if (profileId):
        my_id= str(profileId)+str(query_result['date2'])+str(current_tim2)+str(query_result['trans_id'])
    else:
        my_id= str(query_result['user'])+str(query_result['date2'])+str(current_tim2)+str(query_result['trans_id'])

    # pdf_type = "deposit"
    # pdf_type = query_result['TXN_CODE']
    # argument = __get_argument(pdf_type,images)
    # argument = int(argument)

    # sign_result, stamp_result, tesser_amount_word, decoded_line_am, decoded_line_denoiser, tesser_amount_fig, pdf_date = numbers_to_strings(argument, "ticket.jpg")



    if(status=="True"):
        msg = "stamp Not Found"
        Exp_id = 41
        # if(stamp_result):
        #     msg = "Ticket is not signed"
        #     Exp_id = 40
        #     if(sign_result):
        #         msg = "Amount on ticket is not matched with transection"
        #         Exp_id = 33
        #         if(tesser_amount_fig == query_result['credit_amount']):
        #             msg = "Date is incorrect"
        #             if(pdf_date == query_result['date'] or argument == 5 or argument == 6):
        #                 msg = "Amount in words and fig is not matched"
        #                 if(tesser_amount_fig == tesser_amount_word or argument == 6):
        branchCode=query_result['branch']
        initialdate=query_result['date']
        grpbuuser=query_result['user']
        __update_callover(id,  my_id, today, todaye,username,branchCode,initialdate,grpbuuser)
        useractivity(request.session.session_key,"Callover for Tellers",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
    request.session['username'],
    today_date,"""{0} called over transaction {1}""".format(request.session['username'],query_result['trans_id']),
    "Callover for Tellers",request.session.session_key,"U-review","Callover",today,today_date)
        accepted_transection = IC4_ACCEPTED_CALLOVER(CallOver_ID=my_id,Callover_Officer=username,
                                                                         GRP_BY_REF=query_result['trans_id'],
                                                                         GRP_BY_USER=query_result['user'],
                                                                         GRP_BY_DATE=query_result['date'],
                                                                         Branch_Code=query_result['branch'],
                                                                         Ref_Num=voucher,
                                                                         Tree_Key=4581)
        accepted_transection.save()
       
        flag = True
        msg = ""
        
        
        exception_dict = ""
        if(flag==False):
            exception = IC4_Observation_Model.objects.get(pk=20)
            def obj_to_dict(obj):
                return obj.__dict__
            json_string = json.dumps(exception, default=obj_to_dict)
            exception_dict = json.loads(json_string)

            

               
            
        # exception_dict = ""
        if (inputterEmail):
    
            args = {
            'flag': flag,
            'msg': msg,
            'exception_result': exception_dict,
            'query_result': query_result,
            'today_date': todayc,
            'tomorrow': tomorrowf,
            'callover': username,
            'inputterEmail': inputterEmail,
            'profileId': profileId, 
            'current_tim2': current_tim2
            
            
        }
        else:
            args = {
            'flag': flag,
            'msg': msg,
            'exception_result': exception_dict,
            'query_result': query_result,
            'today_date': todayc,
            'tomorrow': tomorrowf,
            'callover': username,
            'inputterEmail': 'u-review@unionbankng.com',
            'profileId': profileId, 
            'current_tim2': current_tim2
            
            
        }
    return JsonResponse(args)


@csrf_exempt
def OCR2(request):
    print("=====================================================")
    print(request.POST['status'])
    username=request.session['userparam']
    todayd = datetime.now().date()
    todayc=todayd.strftime("%d-%m-%Y")
    today = datetime.now().date()
    t = time.localtime()
    tomorrow = today + timedelta(days=1)
    tomorrowf=tomorrow.strftime("%d-%m-%Y")
    current_time = time.strftime("%H:%M:%S", t)
    todaye=time.strftime("%Y-%m-%d %H:%M:%S", t)

    addt='000'
    current_tim = time.strftime("%H%M", t)
    current_tim2=current_tim+addt
    flag = False
    id = request.POST['id']
    # pdf = request.POST['pdf']
    voucher = request.POST['voucher']
    status = request.POST['status']

    query_result = __get_query_result(id)
    date_only = query_result['date'].strftime("%d-%m-%Y")
    callover_ID = str(query_result['user']) + str(date_only) + query_result['trans_id']

    # bytes = b64decode(pdf, validate=True)
    # images = convert_from_bytes(bytes)
    # img  = images[0]
    request.session['review'] =tomorrowf


    users = query_result['user']
    results = Profile.objects.filter(Profile_ID=users)
    profileId=''
    inputterEmail=''
    for result in results:
        inputterEmail = result.Email
        profileId=result.Profile_ID
    
    obt={
        'rest':IC4_Observation_Model.objects.all()
        
    }
    if (profileId):
        my_id= str(profileId)+str(query_result['date2'])+str(current_tim2)+str(query_result['trans_id'])
    else:
        my_id= str(query_result['user'])+str(query_result['date2'])+str(current_tim2)+str(query_result['trans_id'])

    # pdf_type = "deposit"
    # pdf_type = query_result['TXN_CODE']
    # argument = __get_argument(pdf_type,images)
    # argument = int(argument)

    # sign_result, stamp_result, tesser_amount_word, decoded_line_am, decoded_line_denoiser, tesser_amount_fig, pdf_date = numbers_to_strings(argument, "ticket.jpg")



    if(status=="True"):
        msg = "stamp Not Found"
        Exp_id = 41
        # if(stamp_result):
        #     msg = "Ticket is not signed"
        #     Exp_id = 40
        #     if(sign_result):
        #         msg = "Amount on ticket is not matched with transection"
        #         Exp_id = 33
        #         if(tesser_amount_fig == query_result['credit_amount']):
        #             msg = "Date is incorrect"
        #             if(pdf_date == query_result['date'] or argument == 5 or argument == 6):
        #                 msg = "Amount in words and fig is not matched"
        #                 if(tesser_amount_fig == tesser_amount_word or argument == 6):
        # __update_callover(id,  my_id, today, todaye,username)

        # accepted_transection = IC4_ACCEPTED_CALLOVER(CallOver_ID=my_id,Callover_Officer=username,
        #                                                                  GRP_BY_REF=query_result['trans_id'],
        #                                                                  GRP_BY_USER=query_result['user'],
        #                                                                  GRP_BY_DATE=query_result['date'],
        #                                                                  Branch_Code=query_result['branch'],
        #                                                                  Ref_Num=voucher,
        #                                                                  Tree_Key=4581)
        # accepted_transection.save()
       
        flag = True
        msg = ""
        
        
        exception_dict = ""
        if(flag==False):
            exception = IC4_Observation_Model.objects.get(pk=20)
            def obj_to_dict(obj):
                return obj.__dict__
            json_string = json.dumps(exception, default=obj_to_dict)
            exception_dict = json.loads(json_string)

            

               
            
        # exception_dict = ""
        if (inputterEmail):
    
            args = {
            'flag': flag,
            'msg': msg,
            'exception_result': exception_dict,
            'query_result': query_result,
            'today_date': todayc,
            'tomorrow': tomorrowf,
            'callover': username,
            'inputterEmail': inputterEmail,
            'profileId': profileId, 
            'current_tim2': current_tim2
            
            
        }
        else:
            args = {
            'flag': flag,
            'msg': msg,
            'exception_result': exception_dict,
            'query_result': query_result,
            'today_date': todayc,
            'tomorrow': tomorrowf,
            'callover': username,
            'inputterEmail': 'u-review@unionbankng.com',
            'profileId': profileId, 
            'current_tim2': current_tim2
            
            
        }




    return JsonResponse(args)









from django.core.mail import send_mail
from datetime import datetime
from django.conf import settings
def exception(request):
    transID = request.POST['transID']
    calloverDate = request.POST['calloverDate']
    reviewDate = request.POST['reviewDate']
    officer = request.POST['officer']
    observation = request.POST['exceptionDetails']
    exceptionDetails = request.POST['observation']
    implication = request.POST['implication']
    severity = request.POST['severity']
    branchCode = request.POST['branchCode']
    enteryDate = request.POST['enteryDate']
    inputterEmail = request.POST['inputter-email']
    action = request.POST['action']

    reviewDate = datetime.strptime(reviewDate, '%Y-%m-%d').date()
    calloverDate = datetime.strptime(calloverDate, '%Y-%m-%d').date()
    enteryDate = enteryDate[0:10]
    enteryDate = datetime.strptime(enteryDate, '%Y-%m-%d').date()

    query_result = __get_query_result(transID)
    date_only = query_result['date'].strftime("%d-%m-%Y")
    callover_ID = str(query_result['user']) + str(date_only) + query_result['trans_id']

    exception_transection = IC4_CALLOVER_EXCEPTION(CallOver_ID=callover_ID, Branch_Code= branchCode, Trans_ID=transID, IC4_Inputter=inputterEmail, Callover_Officer=officer, Severity_Level=severity, Implication=implication, Action=action, Exception_Details=exceptionDetails, Observation=observation, Entery_Date=enteryDate, Callover_Date=calloverDate, Review=reviewDate)

    exception_transection.save()
    # if(request.user.is_authenticated):
    #     subject = 'Exception Details'
    #     message = transID + ' has the following exception \n' + implication
    #     email_from = settings.EMAIL_HOST_USER
    #     recipient_list = [request.user.email]
    #     send_mail(subject, message, email_from, recipient_list, fail_silently=False)
    return redirect('acc_trans',trans_id = transID)

def load(request):
    response = IC4_Callover.objects.all().update(IP_Address='127.0.0.1:8090')
    return HttpResponse("Hello world")

def cash_deposit_slip(im):
    im=im
    im_crop = im.crop((100, 75, 1000, 900))
    return im_crop
def cheque(im):
    im=im
    im_crop = im.crop((50, 0, 1400, 800))
    return im_crop
def In_House_cheque(im):
    im=im
    im_crop = im.crop((50, 0, 1400, 800))
    return im_crop
def withdraw(im):
    im=im
    im_crop = im.crop((50, 0, 1600, 800))
    return im_crop
def transfer(im):
    im=im
    im_crop = im.crop((50, 0, 1400, 800))
    return im_crop
def transfer_form(im):
    im=im
    im_crop = im.crop((50, 0, 1600, 2000))
    return im_crop
def NEFT_transfer(im):
    im=im
    im_crop = im.crop((50, 0, 1600, 2150))
    return im_crop