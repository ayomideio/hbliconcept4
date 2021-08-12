from io import BytesIO


import requests
import time

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


from pendingcalloverforcontrol.models import IC4_ACCEPTED_CALLOVER
from iconcept4.models import Profile,IC4_Observation_Model, IC4_CALLOVER_EXCEPTION,IC4_Callover_L3

# from django.http import HttpResponse, JsonResponse
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd

from .queries import *
from django.db import connection
from django.urls import reverse
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.utils
import random
import socket
from iconcept4.views import useractivity
from datetime import datetime
from iconcept4.views import returnallbranch
today=datetime.date(datetime.now())
date_time=datetime.now()


def index(request):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):
        b_c = ''
        transLimit=request.POST.get('transLimit')
        request.session['transLimit']=0
        
        transLimit=''
        if (request.POST.get('transLimit') is not None):
            transLimit=int(request.POST.get('transLimit'))
        request.session['transLimit']=0
    
        if (transLimit is not  None):
            if type(transLimit) == int or type(transLimit) == float:
                request.session['transLimit']=transLimit
            else:
                request.session['transLimit']=0

        if('transLimit' in request.session):
        
           
            today_date = '19-JUL-18'
            
            b_c=returnallbranch(request.session['secondarybranch'],request.session['username'])
            print(b_c)

            cursor = connection.cursor()
            useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),request.session['username'],
                                    today_date,"""{0} visited the first summary page""".format(request.session['username']),"Callover for Control",request.session.session_key,"U-review",
                                        "Callover",today,today_date)
            request.session['profile']="Select Profile"
            if (request.POST.get('profile')):
                useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
            request.session['username'],
            today_date,"""{0} visited the first summary page and grouped by profile {1}""".format(request.session['username'],
            request.POST.get('profile')),"Callover for Control",request.session.session_key,"U-review",
            "Callover",today,today_date)
                request.session['profile']=request.POST.get('profile')
                tuple11=(request.session['transLimit'],request.POST.get('profile'))
                result = cursor.execute('''
                        SELECT IC4_BRANCH_CODE, GRP_BY_DATE, SUM(CALL_NO_OF_VOUCHERS) as NO_OF_ENTRIES, SUM(CALL_CREDIT_FREQ) as NO_OF_CREDIT, SUM(CALL_DEBIT_FREQ) as NO_OF_DEBIT, TO_CHAR(SUM(CALL_CREDIT_TOTAL), 'FM99,999,999,999,999.00') as CREDIT_TOTAL_CALL, TO_CHAR(SUM(CALL_DEBIT_TOTAL), 'FM99,999,999,999,999.00') as DEBIT_TOTAL_CALL 
                            FROM ( 

                            SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
                            SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, SUM(CREDIT) CALL_CREDIT_TOTAL, 
                            SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, SUM(ABS(DEBIT)) as CALL_DEBIT_TOTAL, 
                            SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE 
                            FROM (  SELECT TRANS_ID GRP_BY_REF,
                            BRANCH_CODE IC4_BRANCH_CODE,
                            ENTRY_DATE GRP_BY_DATE, 
                            IC4_INPUTTER GRP_BY_USER, 
                            CALLOVER_OFFICER, 
                            case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ,
                            case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ,
                            case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT,
                            case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT
                            from (
                            SELECT 
                            ID,
                            TRANS_ID,
                            TRANS_ID as TRANS_ID_1,
                            entry_time,
                            TRANS_ID as TRANS_REF_ID,                                                    
                            TRANS_REF_ID AS REF_ID,                                                      
                            TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                            BRANCH_CODE,                                                                                             
                                                                                
                            ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                            ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                            LCY_CODE AS TXN_CCY,   
                            FCY_AMOUNT AMT_1,             
                            FCY_CODE,             
                            TRANS_CODE  AS TXN_C,                                    
                            trans_id as TRN_REF_NO,                                    
                            CHEQUE_NO,                           
                            NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                            VALUE_DATE,                
                            BOOKING_DATE,              
                            POSTING_DATE,              
                            ENTRY_DATE,                
                                            
                            IC4_ACCOUNT_OFFICER,                 
                            IC4_INPUTTER ,                        
                            IC4_AUTHORISER ,                      
                            IC4_VERIFIER  ,
                            CHECKER_ID, 
                            MAKER_ID,                       
                            TEXT_FIELD_1  ,                                                      
                            TEXT_FIELD_2, 
                            AMT_FIELD_1,                                                     
                            to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                            to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                            AMT_FIELD_2,           
                            DATE_FIELD_1,              
                            DATE_FIELD_2 ,             
                            CALLOVER_REMARK,                                                                                      
                            EXCEPTION_ID,                                                      
                            SEVERITY_ID,                                                       
                            REVIEW_DATE,               
                            CALLOVER_OFFICER,                                                                                                         
                            CALLOVER_DATE,             
                            CALLOVER_TIME,             
                            IC4_SPECIAL,                         
                                                                                                                    
                            CHECKER_DATE_TIME,         
                            CALLOVER_ID,                                                                                          
                            POST_BRN,                                                          
                            BATCH_NO,                                                          
                            V_NUM,                                                             
                            DOC_NO,               
                            DR_TXN_NGN,             
                            RATE,                   
                            TXN_MNEM AS MNEM,             
                            AC_GL_BRN_NAME,                                                    
                            COD_BANK,             
                            TXN_MNEMONIC AS BRN_TXN,                                                      
                            TXN_BRANCH,                                                        
                            AMOUNT,                 
                            TIME_KEY AS TENOR,               
                            TRAN_DATE ,
                            branch_name  

                            

                            FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                            WHERE  A.BRANCH_CODE IN ({0})
                        
                            AND A.TXN_MNEMONIC='NORMAL'
                            AND A.CALLOVER_OFFICER IS NULL
                            AND EXISTS ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 B
                                    WHERE  B.BRANCH_CODE = A.BRANCH_CODE 
                                    AND TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')
                                    AND B.TRANS_ID = A.TRANS_ID
                                    AND A.TXN_MNEMONIC = 'NORMAL'
                                    AND ABS(B.AMT_FIELD_1) >= %s
                                    AND B.CALLOVER_OFFICER IS NULL 
                                )
                            AND A.IC4_INPUTTER = %s
                            ) a  ) a 
                            GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                            ) GROUP BY GRP_BY_DATE, IC4_BRANCH_CODE
                            ORDER BY GRP_BY_DATE, IC4_BRANCH_CODE

                    '''.format(b_c),(request.session['transLimit'],request.POST.get('profile')))
            
            else:
                result = cursor.execute('''
                        SELECT IC4_BRANCH_CODE, GRP_BY_DATE, SUM(CALL_NO_OF_VOUCHERS) as NO_OF_ENTRIES, SUM(CALL_CREDIT_FREQ) as NO_OF_CREDIT, SUM(CALL_DEBIT_FREQ) as NO_OF_DEBIT, TO_CHAR(SUM(CALL_CREDIT_TOTAL), 'FM99,999,999,999,999.00') as CREDIT_TOTAL_CALL, TO_CHAR(SUM(CALL_DEBIT_TOTAL), 'FM99,999,999,999,999.00') as DEBIT_TOTAL_CALL 
                            FROM ( 

                            SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
                            SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, SUM(CREDIT) CALL_CREDIT_TOTAL, 
                            SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, SUM(ABS(DEBIT)) as CALL_DEBIT_TOTAL, 
                            SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE 
                            FROM (  SELECT TRANS_ID GRP_BY_REF,
                            BRANCH_CODE IC4_BRANCH_CODE,
                            ENTRY_DATE GRP_BY_DATE, 
                            IC4_INPUTTER GRP_BY_USER, 
                            CALLOVER_OFFICER, 
                            case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ,
                            case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ,
                            case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT,
                            case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT
                            from (
                            SELECT 
                            ID,
                            TRANS_ID,
                            TRANS_ID as TRANS_ID_1,
                            entry_time,
                            TRANS_ID as TRANS_REF_ID,                                                    
                            TRANS_REF_ID AS REF_ID,                                                      
                            TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                            BRANCH_CODE,                                                                                             
                                                                                
                            ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                            ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                            LCY_CODE AS TXN_CCY,   
                            FCY_AMOUNT AMT_1,             
                            FCY_CODE,             
                            TRANS_CODE  AS TXN_C,                                    
                            trans_id as TRN_REF_NO,                                    
                            CHEQUE_NO,                           
                            NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                            VALUE_DATE,                
                            BOOKING_DATE,              
                            POSTING_DATE,              
                            ENTRY_DATE,                
                                            
                            IC4_ACCOUNT_OFFICER,                 
                            IC4_INPUTTER ,                        
                            IC4_AUTHORISER ,                      
                            IC4_VERIFIER  ,
                            CHECKER_ID, 
                            MAKER_ID,                       
                            TEXT_FIELD_1  ,                                                      
                            TEXT_FIELD_2, 
                            AMT_FIELD_1,                                                     
                            to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                            to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                            AMT_FIELD_2,           
                            DATE_FIELD_1,              
                            DATE_FIELD_2 ,             
                            CALLOVER_REMARK,                                                                                      
                            EXCEPTION_ID,                                                      
                            SEVERITY_ID,                                                       
                            REVIEW_DATE,               
                            CALLOVER_OFFICER,                                                                                                         
                            CALLOVER_DATE,             
                            CALLOVER_TIME,             
                            IC4_SPECIAL,                         
                                                                                                                    
                            CHECKER_DATE_TIME,         
                            CALLOVER_ID,                                                                                          
                            POST_BRN,                                                          
                            BATCH_NO,                                                          
                            V_NUM,                                                             
                            DOC_NO,               
                            DR_TXN_NGN,             
                            RATE,                   
                            TXN_MNEM AS MNEM,             
                            AC_GL_BRN_NAME,                                                    
                            COD_BANK,             
                            TXN_MNEMONIC AS BRN_TXN,                                                      
                            TXN_BRANCH,                                                        
                            AMOUNT,                 
                            TIME_KEY AS TENOR,               
                            TRAN_DATE ,
                            branch_name  

                            

                            FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                            WHERE  A.BRANCH_CODE IN ({0}) 
                            AND A.TXN_MNEMONIC='NORMAL' 
                            AND A.CALLOVER_OFFICER IS NULL
                            AND EXISTS ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 B
                                    WHERE  B.BRANCH_CODE = A.BRANCH_CODE 
                                    AND TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')
                                    AND B.TRANS_ID = A.TRANS_ID
                                    AND B.TXN_MNEMONIC='NORMAL'
                                    AND ABS(B.AMT_FIELD_1) >=%(translimit)s
                                    AND B.CALLOVER_OFFICER IS NULL 
                                    )
                            ) a  ) a 
                            GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                            ) GROUP BY GRP_BY_DATE, IC4_BRANCH_CODE
                            ORDER BY GRP_BY_DATE, IC4_BRANCH_CODE

                    '''.format(b_c),{'translimit':request.session['transLimit']} )
            

            yList = dictfetchall(cursor)
        
            columns = [col[0] for col in cursor.description]
            # print(yList)
            # profiles = IC4_Profile.objects.all()
            cursor_profile=connection.cursor()
            profileresult=cursor_profile.execute('''
                        SELECT DISTINCT
                        T.BRANCH_CODE,
                        T.IC4_INPUTTER,
                        coalesce(P.USER_NAME,T.IC4_INPUTTER) PROFILE_NAME
                        FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 T 
                        LEFT JOIN U_IC4INDEP.PROFILE P 
                        ON UPPER(T.IC4_INPUTTER) = UPPER(P.PROFILE_ID)
                        WHERE T.BRANCH_CODE IN ({0}) 
                        AND T.TXN_MNEMONIC = 'NORMAL'
                    
                        AND T.CALLOVER_OFFICER IS NULL                    
                        ORDER BY T.BRANCH_CODE, coalesce(P.USER_NAME,T.IC4_INPUTTER) ASC

                    '''.format(b_c))
            profiles = dictfetchall(profileresult)
            
            
        
            return render(request, 'calloverforcontrol_book/library.html', {'prof_session':request.session['profile'],'results':yList,'transLimit':request.session['transLimit'], 'Profiles':profiles, 'test':'branch_cd','username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
    else:
                # useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
        #             request.session['username'],
        #             "today_date","""session timed out on {0}""".format(request.session['username']),"Callover for Control",request.session.session_key,"U-review",
        #             "Callover",today,"today_date")
        return HttpResponseRedirect(reverse('login'))

   

    
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

# @staff_member_required
def Bank_Trans(request, branch_id):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):
        transactionDate=request.POST.get('dateVal')
        request.session['transactionDate']=transactionDate
        print(transactionDate,"transactionDaste")
        print(request.POST.get('profile'),"profile")
        print(branch_id,"branch_id")
        
        request.session['arraytest']=""
        query = trans_query(branch_id)
        cursor = connection.cursor()
        useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
            request.session['username'],
            today_date,"""{0} visited the second summary page after clicking on branch {1} from the first summary page""".format(request.session['username'],
            branch_id),"Callover for Control",request.session.session_key,"U-review",
            "Callover",today,today_date)
        request.session['selectedbranch'] =branch_id
        print(request.session['profile'])
        if(request.POST.get('profile')):
            print("yes post profile")
            useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
            request.session['username'],
            today_date,"""{0} visited the second summary page after clicking on branch {1} from the first summary page and grouped the transaction by selecting profile {2}""".format(request.session['username'],
            branch_id,request.POST.get('profile')),"Callover for Control",request.session.session_key,"U-review",
            "Callover",today,today_date)
            request.session['profile']=request.POST.get('profile')
            get_byProfile=connection.cursor()
            prof_res=get_byProfile.execute("""  
                        SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
                                    SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, TO_CHAR(SUM(CREDIT), 'FM99,999,999,999,999.00') as CALL_CREDIT_TOTAL, 
                                    SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, TO_CHAR(SUM(ABS(DEBIT)), 'FM99,999,999,999,999.00') as CALL_DEBIT_TOTAL, 
                                    SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE 
                                    FROM (  SELECT TRANS_ID GRP_BY_REF,
                                    BRANCH_CODE IC4_BRANCH_CODE,
                                    ENTRY_DATE GRP_BY_DATE, 
                                    IC4_INPUTTER GRP_BY_USER, 
                                    CALLOVER_OFFICER, 
                                    case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ,
                                    case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ,
                                    case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT,
                                    case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT
                                    from (
                                    SELECT 
                                    ID,
                                    TRANS_ID,
                                    TRANS_ID as TRANS_ID_1,
                                    entry_time,
                                    TRANS_ID as TRANS_REF_ID,                                                    
                                    TRANS_REF_ID AS REF_ID,                                                      
                                    TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                                    BRANCH_CODE,                                                                                             
                                                                                        
                                    ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                    ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                    LCY_CODE AS TXN_CCY,   
                                    FCY_AMOUNT AMT_1,             
                                    FCY_CODE,             
                                    TRANS_CODE  AS TXN_C,                                    
                                    trans_id as TRN_REF_NO,                                    
                                    CHEQUE_NO,                           
                                    NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                                    VALUE_DATE,                
                                    BOOKING_DATE,              
                                    POSTING_DATE,              
                                    TO_CHAR(ENTRY_DATE, 'YYYY-MM-DD') ENTRY_DATE,                
                                                    
                                    IC4_ACCOUNT_OFFICER,                 
                                    IC4_INPUTTER ,                        
                                    IC4_AUTHORISER ,                      
                                    IC4_VERIFIER  ,
                                    CHECKER_ID, 
                                    MAKER_ID,                       
                                    TEXT_FIELD_1  ,                                                      
                                    TEXT_FIELD_2, 
                                    AMT_FIELD_1,                                                     
                                    to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                                    to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                                    AMT_FIELD_2,           
                                    DATE_FIELD_1,              
                                    DATE_FIELD_2 ,             
                                    CALLOVER_REMARK,                                                                                      
                                    EXCEPTION_ID,                                                      
                                    SEVERITY_ID,                                                       
                                    REVIEW_DATE,               
                                    CALLOVER_OFFICER,                                                                                                         
                                    CALLOVER_DATE,             
                                    CALLOVER_TIME,             
                                    IC4_SPECIAL,                         
                                                                                                                            
                                    CHECKER_DATE_TIME,         
                                    CALLOVER_ID,                                                                                          
                                    POST_BRN,                                                          
                                    BATCH_NO,                                                          
                                    V_NUM,                                                             
                                    DOC_NO,               
                                    DR_TXN_NGN,             
                                    RATE,                   
                                    TXN_MNEM AS MNEM,             
                                    AC_GL_BRN_NAME,                                                    
                                    COD_BANK,             
                                    TXN_MNEMONIC AS BRN_TXN,                                                      
                                    TXN_BRANCH,                                                        
                                    AMOUNT,                 
                                    TIME_KEY AS TENOR,               
                                    TRAN_DATE ,
                                    branch_name  

                                    FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                                    WHERE  A.BRANCH_CODE = %s
                                    AND TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD') = %s
                                    AND A.TXN_MNEMONIC='NORMAL' AND A.CALLOVER_OFFICER IS NULL
                                    AND EXISTS ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 B
                                                WHERE B.BRANCH_CODE = A.BRANCH_CODE 
                                                AND TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')
                                                AND B.TRANS_ID = A.TRANS_ID 
                                                AND B.TXN_MNEMONIC='NORMAL'
                                                AND ABS(B.AMT_FIELD_1) >= %s
                                        )
                                    AND A.IC4_INPUTTER=%s
                                    ) a  ) a 
                                    GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                                    ORDER BY IC4_BRANCH_CODE, GRP_BY_DATE, GRP_BY_USER, GRP_BY_REF

                                        """,(request.session['selectedbranch'],request.session['transactionDate'],request.session['transLimit'],request.session['profile']))
            yList=dictfetchall(prof_res)
            
            cursor_profile=connection.cursor()
            profileresult=get_byProfile.execute('''
                    SELECT DISTINCT
                        T.BRANCH_CODE,
                        T.IC4_INPUTTER,
                        coalesce(P.USER_NAME,T.IC4_INPUTTER) PROFILE_NAME
                        FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 T 
                        LEFT JOIN U_IC4INDEP.PROFILE P 
                        ON UPPER(T.IC4_INPUTTER) = UPPER(P.PROFILE_ID)
                        WHERE TO_CHAR(T.ENTRY_DATE, 'YYYY-MM-DD') = %s
                        AND T.BRANCH_CODE= %s
                        AND T.CALLOVER_OFFICER IS NULL  
						AND T.TXN_MNEMONIC = 'NORMAL'
                        ORDER BY T.BRANCH_CODE, coalesce(P.USER_NAME,T.IC4_INPUTTER) ASC
                    ''',(request.session['transactionDate'],branch_id))
            profile=dictfetchall(profileresult)
            # print("Ylist of profile",profile)
            return render(request, 'calloverforcontrol/branch_trans.html', {'results': yList,'prof_session':request.session['profile'],'branch_id':request.session['selectedbranch'],'profile':profile,'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
        else:
            if(request.session['profile']  != "Select Profile"):
                useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
                    request.session['username'],
                    today_date,"""{0} visited the second summary page after clicking on branch {1} from the first summary page and selecting profile {2}""".format(request.session['username'],
                    branch_id,request.session['profile']),"Callover for Control",request.session.session_key,"U-review",
                    "Callover",today,today_date)
                print("yes collected profile")
                get_byProfile=connection.cursor()
                prof_res=get_byProfile.execute("""  
                        SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
                                    SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, TO_CHAR(SUM(CREDIT), 'FM99,999,999,999,999.00') as CALL_CREDIT_TOTAL, 
                                    SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, TO_CHAR(SUM(ABS(DEBIT)), 'FM99,999,999,999,999.00') as CALL_DEBIT_TOTAL, 
                                    SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE 
                                    FROM (  SELECT TRANS_ID GRP_BY_REF,
                                    BRANCH_CODE IC4_BRANCH_CODE,
                                    ENTRY_DATE GRP_BY_DATE, 
                                    IC4_INPUTTER GRP_BY_USER, 
                                    CALLOVER_OFFICER, 
                                    case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ,
                                    case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ,
                                    case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT,
                                    case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT
                                    from (
                                    SELECT 
                                    ID,
                                    TRANS_ID,
                                    TRANS_ID as TRANS_ID_1,
                                    entry_time,
                                    TRANS_ID as TRANS_REF_ID,                                                    
                                    TRANS_REF_ID AS REF_ID,                                                      
                                    TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                                    BRANCH_CODE,                                                                                             
                                                                                        
                                    ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                    ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                    LCY_CODE AS TXN_CCY,   
                                    FCY_AMOUNT AMT_1,             
                                    FCY_CODE,             
                                    TRANS_CODE  AS TXN_C,                                    
                                    trans_id as TRN_REF_NO,                                    
                                    CHEQUE_NO,                           
                                    NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                                    VALUE_DATE,                
                                    BOOKING_DATE,              
                                    POSTING_DATE,              
                                    TO_CHAR(ENTRY_DATE, 'YYYY-MM-DD') ENTRY_DATE,                
                                                    
                                    IC4_ACCOUNT_OFFICER,                 
                                    IC4_INPUTTER ,                        
                                    IC4_AUTHORISER ,                      
                                    IC4_VERIFIER  ,
                                    CHECKER_ID, 
                                    MAKER_ID,                       
                                    TEXT_FIELD_1  ,                                                      
                                    TEXT_FIELD_2, 
                                    AMT_FIELD_1,                                                     
                                    to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                                    to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                                    AMT_FIELD_2,           
                                    DATE_FIELD_1,              
                                    DATE_FIELD_2 ,             
                                    CALLOVER_REMARK,                                                                                      
                                    EXCEPTION_ID,                                                      
                                    SEVERITY_ID,                                                       
                                    REVIEW_DATE,               
                                    CALLOVER_OFFICER,                                                                                                         
                                    CALLOVER_DATE,             
                                    CALLOVER_TIME,             
                                    IC4_SPECIAL,                         
                                                                                                                            
                                    CHECKER_DATE_TIME,         
                                    CALLOVER_ID,                                                                                          
                                    POST_BRN,                                                          
                                    BATCH_NO,                                                          
                                    V_NUM,                                                             
                                    DOC_NO,               
                                    DR_TXN_NGN,             
                                    RATE,                   
                                    TXN_MNEM AS MNEM,             
                                    AC_GL_BRN_NAME,                                                    
                                    COD_BANK,             
                                    TXN_MNEMONIC AS BRN_TXN,                                                      
                                    TXN_BRANCH,                                                        
                                    AMOUNT,                 
                                    TIME_KEY AS TENOR,               
                                    TRAN_DATE ,
                                    branch_name  

                                    FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                                    WHERE  A.BRANCH_CODE = %s
                                    AND TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD') = %s
                                    AND A.TXN_MNEMONIC='NORMAL' AND A.CALLOVER_OFFICER IS NULL
                                    AND EXISTS ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 B
                                                WHERE B.BRANCH_CODE = A.BRANCH_CODE 
                                                AND TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')
                                                AND B.TRANS_ID = A.TRANS_ID
                                                AND ABS(B.AMT_FIELD_1) >= %s
                                        )
                                    AND A.IC4_INPUTTER=%s
                                    ) a  ) a 
                                    GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                                    ORDER BY IC4_BRANCH_CODE, GRP_BY_DATE, GRP_BY_USER, GRP_BY_REF

                                        """,(request.session['selectedbranch'],request.session['transactionDate'],request.session['transLimit'],request.session['profile']))
                yList=dictfetchall(prof_res)
                
                cursor_profile=connection.cursor()
                profileresult=get_byProfile.execute('''
                    SELECT DISTINCT
                        T.BRANCH_CODE,
                        T.IC4_INPUTTER,
                        coalesce(P.USER_NAME,T.IC4_INPUTTER) PROFILE_NAME
                        FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 T 
                        LEFT JOIN U_IC4INDEP.PROFILE P 
                        ON UPPER(T.IC4_INPUTTER) = UPPER(P.PROFILE_ID)
                        WHERE TO_CHAR(T.ENTRY_DATE, 'YYYY-MM-DD') = %s
                        AND T.BRANCH_CODE= %s
                        AND T.CALLOVER_OFFICER IS NULL  
						AND T.TXN_MNEMONIC = 'NORMAL'
                        ORDER BY T.BRANCH_CODE, coalesce(P.USER_NAME,T.IC4_INPUTTER) ASC
                        ''',(request.session['transactionDate'],branch_id))
                profile=dictfetchall(profileresult)
                # print("Ylist of profile",profile)
                return render(request, 'calloverforcontrol/branch_trans.html', {'results': yList,'prof_session':request.session['profile'],'branch_id':request.session['selectedbranch'],'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})


            else:
                useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
                    request.session['username'],
                    today_date,"""{0} visited the second summary page after clicking on branch {1} from the first summary page""".format(request.session['username'],
                    branch_id),"Callover for Control",request.session.session_key,"U-review",
                    "Callover",today,today_date)
                
                result = cursor.execute("""
                        SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
                            SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, TO_CHAR(SUM(CREDIT), 'FM99,999,999,999,999.00') as CALL_CREDIT_TOTAL, 
                            SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, TO_CHAR(SUM(ABS(DEBIT)), 'FM99,999,999,999,999.00') as CALL_DEBIT_TOTAL, 
                            SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE 
                            FROM (  SELECT TRANS_ID GRP_BY_REF,
                            BRANCH_CODE IC4_BRANCH_CODE,
                            ENTRY_DATE GRP_BY_DATE, 
                            IC4_INPUTTER GRP_BY_USER, 
                            CALLOVER_OFFICER, 
                            case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ,
                            case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ,
                            case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT,
                            case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT
                            from (
                            SELECT 
                            ID,
                            TRANS_ID,
                            TRANS_ID as TRANS_ID_1,
                            entry_time,
                            TRANS_ID as TRANS_REF_ID,                                                    
                            TRANS_REF_ID AS REF_ID,                                                      
                            TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                            BRANCH_CODE,                                                                                             
                                                                                
                            ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                            ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                            LCY_CODE AS TXN_CCY,   
                            FCY_AMOUNT AMT_1,             
                            FCY_CODE,             
                            TRANS_CODE  AS TXN_C,                                    
                            trans_id as TRN_REF_NO,                                    
                            CHEQUE_NO,                           
                            NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                            VALUE_DATE,                
                            BOOKING_DATE,              
                            POSTING_DATE,              
                            TO_CHAR(ENTRY_DATE, 'YYYY-MM-DD') ENTRY_DATE,                
                                            
                            IC4_ACCOUNT_OFFICER,                 
                            IC4_INPUTTER ,                        
                            IC4_AUTHORISER ,                      
                            IC4_VERIFIER  ,
                            CHECKER_ID, 
                            MAKER_ID,                       
                            TEXT_FIELD_1  ,                                                      
                            TEXT_FIELD_2, 
                            AMT_FIELD_1,                                                     
                            to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                            to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                            AMT_FIELD_2,           
                            DATE_FIELD_1,              
                            DATE_FIELD_2 ,             
                            CALLOVER_REMARK,                                                                                      
                            EXCEPTION_ID,                                                      
                            SEVERITY_ID,                                                       
                            REVIEW_DATE,               
                            CALLOVER_OFFICER,                                                                                                         
                            CALLOVER_DATE,             
                            CALLOVER_TIME,             
                            IC4_SPECIAL,                         
                                                                                                                    
                            CHECKER_DATE_TIME,         
                            CALLOVER_ID,                                                                                          
                            POST_BRN,                                                          
                            BATCH_NO,                                                          
                            V_NUM,                                                             
                            DOC_NO,               
                            DR_TXN_NGN,             
                            RATE,                   
                            TXN_MNEM AS MNEM,             
                            AC_GL_BRN_NAME,                                                    
                            COD_BANK,             
                            TXN_MNEMONIC AS BRN_TXN,                                                      
                            TXN_BRANCH,                                                        
                            AMOUNT,                 
                            TIME_KEY AS TENOR,               
                            TRAN_DATE ,
                            branch_name  

                            

                            FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                            WHERE  A.BRANCH_CODE = %s
                            AND TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD') = %s
                            AND A.TXN_MNEMONIC='NORMAL' AND A.CALLOVER_OFFICER IS NULL

                            AND EXISTS ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 B
                                        WHERE  B.BRANCH_CODE = A.BRANCH_CODE 
                                        AND TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')
                                        AND B.TRANS_ID = A.TRANS_ID
                                        AND ABS(B.AMT_FIELD_1) >= %s
                                )
                            ) a  ) a 
                            GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                            ORDER BY IC4_BRANCH_CODE, GRP_BY_DATE, GRP_BY_USER, GRP_BY_REF
                                        
                            """,(request.session['selectedbranch'],request.session['transactionDate'],request.session['transLimit']))
                
                print("no profile")
                cursor_profile=connection.cursor()
                profileresult=cursor_profile.execute('''
                    SELECT DISTINCT
                        T.BRANCH_CODE,
                        T.IC4_INPUTTER,
                        coalesce(P.USER_NAME,T.IC4_INPUTTER) PROFILE_NAME
                        FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 T 
                        LEFT JOIN U_IC4INDEP.PROFILE P 
                        ON UPPER(T.IC4_INPUTTER) = UPPER(P.PROFILE_ID)
                        WHERE TO_CHAR(T.ENTRY_DATE, 'YYYY-MM-DD') = %s
                        AND T.BRANCH_CODE= %s
                        AND T.CALLOVER_OFFICER IS NULL  
						AND T.TXN_MNEMONIC = 'NORMAL'
                        ORDER BY T.BRANCH_CODE, coalesce(P.USER_NAME,T.IC4_INPUTTER) ASC
                        ''',(request.session['transactionDate'],branch_id))
                profile=dictfetchall(profileresult)
                # print(profile,"Profile")
                # grouplist=''
                request.session['profile']="Select Profile"
                yList = dictfetchall(cursor)
                request.session['arraytest']=""
                # request.session['arraytest']=[{'IC4_BRANCH_CODE': '010', 'GRP_BY_REF': '010CHDP182000006', 'CALLOVER_OFFICER': None, 'GRP_BY_USER': 'CHIAMAECHI', 'CALL_NO_OF_VOUCHERS': 2, 'CALL_CREDIT_FREQ': 1, 'CALL_CREDIT_TOTAL': 2300, 'CALL_DEBIT_FREQ': 1, 'CALL_DEBIT_TOTAL': 2300, 'CALL_DIFFERENCE': 0}, {'IC4_BRANCH_CODE': '010', 'GRP_BY_REF': '010CHDP182000515',  'CALLOVER_OFFICER': None, 'GRP_BY_USER': 'FCAGU', 'CALL_NO_OF_VOUCHERS': 2, 'CALL_CREDIT_FREQ': 1, 'CALL_CREDIT_TOTAL': 4000, 'CALL_DEBIT_FREQ': 1, 'CALL_DEBIT_TOTAL': 4000, 'CALL_DIFFERENCE': 0}]
                # print(yList)

                return render(request, 'calloverforcontrol/branch_trans.html', {'results': yList,'prof_session':request.session['profile'],'branch_id':request.session['selectedbranch'],'profile':profile,'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
        
    else:
        return HttpResponseRedirect(reverse('login'))



# @staff_member_required
def acc_trans(request, trans_id):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):
        b_c = '010'
        today_date = '2018-07-19'

        trans_id = trans_id.strip()
        print('....................',trans_id)
        # br_nc=branch.strip
        # print('branch:',br_nc)
        tst=request.POST.get('vala')
        if(tst):
            request.session['entry_date']=tst
        checkSkip=request.POST.get('checkSkip')
        
        if(checkSkip=="skip"):
            print("skip")

        else:

            vouchers = []
            addresses = []
            cursorr = connection.cursor()
            resultsr = cursorr.execute("""
                    SELECT * FROM U_IC4INDEP.OBSERVATION_MODEL 
                    ORDER BY DESCRIPTION
            """)
            yListr = dictfetchall(resultsr)

            cursors = connection.cursor()
            resultss = cursors.execute("""
            SELECT USER_ID, FIRST_NAME FROM IC4_PRO_USERS lst WHERE BRANCH_CODE = %(branch)s AND USER_ROLE IN('BSM', 'HEADTELLER')
            """,{'branch':request.session['selectedbranch']})
            yLists = dictfetchall(resultss)


            query = acc_query(trans_id)
            cursor = connection.cursor()
            useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
            request.session['username'],
            today_date,"""{0} visited the third summary page after clicking on transaction id {1} from the second summary page""".format(request.session['username'],
            trans_id),"Callover for Control",request.session.session_key,"U-review",
            "Callover",today,today_date)
            if(request.session['profile']=="Select Profile"):
                useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
                    request.session['username'],
                    today_date,"""{0} visited the third summary page after clicking on transaction id {1} from the second summary page with no selected profile""".format(request.session['username'],
                    trans_id),"Callover for Control",request.session.session_key,"U-review",
                    "Callover",today,today_date)
                results = cursor.execute("""

            
                            
                        SELECT 
                            ID,
                            TRANS_ID,
                            TRANS_ID as TRANS_ID_1,
                            entry_time,
                            TRANS_ID as TRANS_REF_ID,                                                    
                            TRANS_REF_ID AS REF_ID,                                                      
                            TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                            BRANCH_CODE,                                                                                             
                                                                                
                            ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                            ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                            LCY_CODE AS TXN_CCY,   
                            FCY_AMOUNT AMT_1,             
                            FCY_CODE,             
                            TRANS_CODE  AS TXN_C,                                    
                            trans_id as TRN_REF_NO,                                    
                            CHEQUE_NO,                           
                            NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                            VALUE_DATE,                
                            BOOKING_DATE,              
                            POSTING_DATE,              
                            ENTRY_DATE,                
                                            
                            IC4_ACCOUNT_OFFICER,                 
                            IC4_INPUTTER ,                        
                            IC4_AUTHORISER ,                      
                            IC4_VERIFIER  ,
                            CHECKER_ID, 
                            MAKER_ID,                       
                            TEXT_FIELD_1  ,                                                      
                            TEXT_FIELD_2, 
                            AMT_FIELD_1,                                                     
                            to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                            to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                            AMT_FIELD_2,           
                            DATE_FIELD_1,              
                            DATE_FIELD_2 ,             
                            CALLOVER_REMARK,                                                                                      
                            EXCEPTION_ID,                                                      
                            SEVERITY_ID,                                                       
                            REVIEW_DATE,               
                            CALLOVER_OFFICER,                                                                                                         
                            CALLOVER_DATE,             
                            CALLOVER_TIME,             
                            IC4_SPECIAL,                         
                                                                                                                    
                            CHECKER_DATE_TIME,         
                            CALLOVER_ID,                                                                                          
                            POST_BRN,                                                          
                            BATCH_NO,                                                          
                            V_NUM,                                                             
                            DOC_NO,               
                            DR_TXN_NGN,             
                            RATE,                   
                            TXN_MNEM AS MNEM,             
                            AC_GL_BRN_NAME,                                                    
                            COD_BANK,             
                            TXN_MNEMONIC AS BRN_TXN,                                                      
                            TXN_BRANCH,                                                        
                            AMOUNT,                 
                            TIME_KEY AS TENOR,               
                            TRAN_DATE ,
                            branch_name  

                            

                            FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                            WHERE  A.BRANCH_CODE = %s
                            AND A.TRANS_ID =%s
                            AND TRUNC(A.ENTRY_DATE)=%s
                            AND A.TXN_MNEMONIC='NORMAL' AND A.CALLOVER_OFFICER IS NULL

                        """,(request.session['selectedbranch'] ,trans_id,request.session['entry_date']))
            else:
                useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
                        request.session['username'],
                        today_date,"""{0} visited the third summary page after clicking on transaction id {1} from the second summary page and selected profile {2}""".format(request.session['username'],
                        trans_id,request.session['profile']),"Callover for Control",request.session.session_key,"U-review",
                        "Callover",today,today_date)
                results = cursor.execute("""

            
                            
                        SELECT 
                            ID,
                            TRANS_ID,
                            TRANS_ID as TRANS_ID_1,
                            entry_time,
                            TRANS_ID as TRANS_REF_ID,                                                    
                            TRANS_REF_ID AS REF_ID,                                                      
                            TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                            BRANCH_CODE,                                                                                             
                                                                                
                            ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                            ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                            LCY_CODE AS TXN_CCY,   
                            FCY_AMOUNT AMT_1,             
                            FCY_CODE,             
                            TRANS_CODE  AS TXN_C,                                    
                            trans_id as TRN_REF_NO,                                    
                            CHEQUE_NO,                           
                            NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                            VALUE_DATE,                
                            BOOKING_DATE,              
                            POSTING_DATE,              
                            ENTRY_DATE,                
                                            
                            IC4_ACCOUNT_OFFICER,                 
                            IC4_INPUTTER ,                        
                            IC4_AUTHORISER ,                      
                            IC4_VERIFIER  ,
                            CHECKER_ID, 
                            MAKER_ID,                       
                            TEXT_FIELD_1  ,                                                      
                            TEXT_FIELD_2, 
                            AMT_FIELD_1,                                                     
                            to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                            to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                            AMT_FIELD_2,           
                            DATE_FIELD_1,              
                            DATE_FIELD_2 ,             
                            CALLOVER_REMARK,                                                                                      
                            EXCEPTION_ID,                                                      
                            SEVERITY_ID,                                                       
                            REVIEW_DATE,               
                            CALLOVER_OFFICER,                                                                                                         
                            CALLOVER_DATE,             
                            CALLOVER_TIME,             
                            IC4_SPECIAL,                         
                                                                                                                    
                            CHECKER_DATE_TIME,         
                            CALLOVER_ID,                                                                                          
                            POST_BRN,                                                          
                            BATCH_NO,                                                          
                            V_NUM,                                                             
                            DOC_NO,               
                            DR_TXN_NGN,             
                            RATE,                   
                            TXN_MNEM AS MNEM,             
                            AC_GL_BRN_NAME,                                                    
                            COD_BANK,             
                            TXN_MNEMONIC AS BRN_TXN,                                                      
                            TXN_BRANCH,                                                        
                            AMOUNT,                 
                            TIME_KEY AS TENOR,               
                            TRAN_DATE ,
                            branch_name  

                            

                            FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                            WHERE  A.BRANCH_CODE = %s
                            AND A.TRANS_ID =%s
                            AND TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')=%s
                            AND A.IC4_INPUTTER = %s
                            AND A.TXN_MNEMONIC='NORMAL' AND A.CALLOVER_OFFICER IS NULL

                        """,(request.session['selectedbranch'] ,trans_id,request.session['entry_date'],request.session['profile']))

      
            cursor2=connection.cursor()
            secondtrans_id=cursor2.execute("""

            
                            
                        SELECT 
                            ID,
                            TRANS_ID,
                            TRANS_ID as TRANS_ID_1,
                            entry_time,
                            TRANS_ID as TRANS_REF_ID,                                                    
                            TRANS_REF_ID AS REF_ID,                                                      
                            TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                            BRANCH_CODE,                                                                                             
                                                                                
                            ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                            ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                            LCY_CODE AS TXN_CCY,   
                            FCY_AMOUNT AMT_1,             
                            FCY_CODE,             
                            TRANS_CODE  AS TXN_C,                                    
                            trans_id as TRN_REF_NO,                                    
                            CHEQUE_NO,                           
                            NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                            VALUE_DATE,                
                            BOOKING_DATE,              
                            POSTING_DATE,              
                            ENTRY_DATE,                
                                            
                            IC4_ACCOUNT_OFFICER,                 
                            IC4_INPUTTER ,                        
                            IC4_AUTHORISER ,                      
                            IC4_VERIFIER  ,
                            CHECKER_ID, 
                            MAKER_ID,                       
                            TEXT_FIELD_1  ,                                                      
                            TEXT_FIELD_2, 
                            AMT_FIELD_1,                                                     
                            to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                            to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                            AMT_FIELD_2,           
                            DATE_FIELD_1,              
                            DATE_FIELD_2 ,             
                            CALLOVER_REMARK,                                                                                      
                            EXCEPTION_ID,                                                      
                            SEVERITY_ID,                                                       
                            REVIEW_DATE,               
                            CALLOVER_OFFICER,                                                                                                         
                            CALLOVER_DATE,             
                            CALLOVER_TIME,             
                            IC4_SPECIAL,                         
                                                                                                                    
                            CHECKER_DATE_TIME,         
                            CALLOVER_ID,                                                                                          
                            POST_BRN,                                                          
                            BATCH_NO,                                                          
                            V_NUM,                                                             
                            DOC_NO,               
                            DR_TXN_NGN,             
                            RATE,                   
                            TXN_MNEM AS MNEM,             
                            AC_GL_BRN_NAME,                                                    
                            COD_BANK,             
                            TXN_MNEMONIC AS BRN_TXN,                                                      
                            TXN_BRANCH,                                                        
                            AMOUNT,                 
                            TIME_KEY AS TENOR,               
                            TRAN_DATE ,
                            branch_name  

                            

                            FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                            WHERE  A.BRANCH_CODE = %s

                            AND A.TRANS_ID =%s
                            AND TRUNC(A.ENTRY_DATE)=%s
                            AND A.TXN_MNEMONIC='NORMAL' AND A.CALLOVER_OFFICER IS NULL

                    """,(request.session['selectedbranch'] ,trans_id,request.session['entry_date']))
            list2=cursor2.fetchone()
            # print(list2[2])
            yList = dictfetchall(results)
            print("a")
            # print(yList)
            print("b")
            if (yList):
                
        
                tst=""" date={1}  data2={0} """.format(trans_id,today_date)
                # print(tst)
                # print("yList:",yList)
                transections = IC4_Callover_L3.objects.filter(Trans_ID=trans_id)
                request.session['tranid'] =b_c
                # for t in transections:
                #     vouchers.append(t.Ref_Num)
                #     # print("Ref_Num:", t.Ref_Num)
                #     addresses.append(t.IP_Address)
                #     # print("IP_Address:", t.IP_Address)
                # voucher_id = vouchers[0]
                # IP_Address = addresses[0]
                return render(request, 'calloverforcontrol/acc_trans.html', {'branch_id':request.session['selectedbranch'],'prof_session':request.session['profile'],'calloverurl':request.session['calloverurl'],'tran':request.session['selectedbranch'],'cb':request.session['arraytest'],'results': yList,'username':request.session['userparam'],  'trans_ID':list2[2],'yListr':yListr,'yLists':yLists,'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
            else:
                if(request.session['profile']=="Select Profile"):
                    yList=None
                    cursor2 = connection.cursor()
                    cursor2.execute(""" SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
                                SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, TO_CHAR(SUM(CREDIT), 'FM99,999,999,999,999.00') as CALL_CREDIT_TOTAL, 
                                SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, TO_CHAR(SUM(ABS(DEBIT)), 'FM99,999,999,999,999.00') as CALL_DEBIT_TOTAL, 
                                SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE 
                                FROM (  SELECT TRANS_ID GRP_BY_REF,
                                BRANCH_CODE IC4_BRANCH_CODE,
                                ENTRY_DATE GRP_BY_DATE, 
                                IC4_INPUTTER GRP_BY_USER, 
                                CALLOVER_OFFICER, 
                                case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ,
                                case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ,
                                case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT,
                                case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT
                                from (
                                SELECT 
                                ID,
                                TRANS_ID,
                                TRANS_ID as TRANS_ID_1,
                                entry_time,
                                TRANS_ID as TRANS_REF_ID,                                                    
                                TRANS_REF_ID AS REF_ID,                                                      
                                TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                                BRANCH_CODE,                                                                                             
                                                                                    
                                ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                LCY_CODE AS TXN_CCY,   
                                FCY_AMOUNT AMT_1,             
                                FCY_CODE,             
                                TRANS_CODE  AS TXN_C,                                    
                                trans_id as TRN_REF_NO,                                    
                                CHEQUE_NO,                           
                                NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                                VALUE_DATE,                
                                BOOKING_DATE,              
                                POSTING_DATE,              
                                TO_CHAR(ENTRY_DATE, 'YYYY-MM-DD') ENTRY_DATE,                
                                                
                                IC4_ACCOUNT_OFFICER,                 
                                IC4_INPUTTER ,                        
                                IC4_AUTHORISER ,                      
                                IC4_VERIFIER  ,
                                CHECKER_ID, 
                                MAKER_ID,                       
                                TEXT_FIELD_1  ,                                                      
                                TEXT_FIELD_2, 
                                AMT_FIELD_1,                                                     
                                to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                                to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                                AMT_FIELD_2,           
                                DATE_FIELD_1,              
                                DATE_FIELD_2 ,             
                                CALLOVER_REMARK,                                                                                      
                                EXCEPTION_ID,                                                      
                                SEVERITY_ID,                                                       
                                REVIEW_DATE,               
                                CALLOVER_OFFICER,                                                                                                         
                                CALLOVER_DATE,             
                                CALLOVER_TIME,             
                                IC4_SPECIAL,                         
                                                                                                                        
                                CHECKER_DATE_TIME,         
                                CALLOVER_ID,                                                                                          
                                POST_BRN,                                                          
                                BATCH_NO,                                                          
                                V_NUM,                                                             
                                DOC_NO,               
                                DR_TXN_NGN,             
                                RATE,                   
                                TXN_MNEM AS MNEM,             
                                AC_GL_BRN_NAME,                                                    
                                COD_BANK,             
                                TXN_MNEMONIC AS BRN_TXN,                                                      
                                TXN_BRANCH,                                                        
                                AMOUNT,                 
                                TIME_KEY AS TENOR,               
                                TRAN_DATE ,
                                branch_name  

                                

                                FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                                WHERE  A.BRANCH_CODE = %(branchcode)s
                                AND TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD') = %(dater)s
                                AND A.TXN_MNEMONIC='NORMAL' AND A.CALLOVER_OFFICER IS NULL
                                    
                                ) a  ) a 
                                GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                                ORDER BY IC4_BRANCH_CODE, GRP_BY_DATE, GRP_BY_USER, GRP_BY_REF
                                    
                """,{'branchcode':request.session['selectedbranch'],'dater':request.session['transactionDate']})
                    list2=cursor2.fetchone()
                    if (list2):
                        cursor13 = connection.cursor()
                        useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
                                request.session['username'],
                                today_date,"""{0} re-visited the third summary page after clicking next transaction {1} and did not select any profile""".format(request.session['username'],
                                list2[1],request.session['profile']),"Callover for Control",request.session.session_key,"U-review",
                                "Callover",today,today_date)
                        cursor13.execute("""
                                        SELECT 
                                    ID,
                                    TRANS_ID,
                                    TRANS_ID as TRANS_ID_1,
                                    entry_time,
                                    TRANS_ID as TRANS_REF_ID,                                                    
                                    TRANS_REF_ID AS REF_ID,                                                      
                                    TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                                    BRANCH_CODE,                                                                                             
                                                                                        
                                    ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                    ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                    LCY_CODE AS TXN_CCY,   
                                    FCY_AMOUNT AMT_1,             
                                    FCY_CODE,             
                                    TRANS_CODE  AS TXN_C,                                    
                                    trans_id as TRN_REF_NO,                                    
                                    CHEQUE_NO,                           
                                    NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                                    VALUE_DATE,                
                                    BOOKING_DATE,              
                                    POSTING_DATE,              
                                    ENTRY_DATE,                
                                                    
                                    IC4_ACCOUNT_OFFICER,                 
                                    IC4_INPUTTER ,                        
                                    IC4_AUTHORISER ,                      
                                    IC4_VERIFIER  ,
                                    CHECKER_ID, 
                                    MAKER_ID,                       
                                    TEXT_FIELD_1  ,                                                      
                                    TEXT_FIELD_2, 
                                    AMT_FIELD_1,                                                     
                                    to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                                    to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                                    AMT_FIELD_2,           
                                    DATE_FIELD_1,              
                                    DATE_FIELD_2 ,             
                                    CALLOVER_REMARK,                                                                                      
                                    EXCEPTION_ID,                                                      
                                    SEVERITY_ID,                                                       
                                    REVIEW_DATE,               
                                    CALLOVER_OFFICER,                                                                                                         
                                    CALLOVER_DATE,             
                                    CALLOVER_TIME,             
                                    IC4_SPECIAL,                         
                                                                                                                            
                                    CHECKER_DATE_TIME,         
                                    CALLOVER_ID,                                                                                          
                                    POST_BRN,                                                          
                                    BATCH_NO,                                                          
                                    V_NUM,                                                             
                                    DOC_NO,               
                                    DR_TXN_NGN,             
                                    RATE,                   
                                    TXN_MNEM AS MNEM,             
                                    AC_GL_BRN_NAME,                                                    
                                    COD_BANK,             
                                    TXN_MNEMONIC AS BRN_TXN,                                                      
                                    TXN_BRANCH,                                                        
                                    AMOUNT,                 
                                    TIME_KEY AS TENOR,               
                                    TRAN_DATE ,
                                    branch_name  

                                    

                                    FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                                    WHERE  A.BRANCH_CODE = %s
                                    AND A.TRANS_ID =%s
                                    AND TRUNC(A.ENTRY_DATE)=%s
                                    AND A.CALLOVER_OFFICER IS NULL
                                    """,(request.session['selectedbranch'],list2[1],list2[2]))
                        
                        cursor14=connection.cursor()
                        cursor14.execute("""
                                        SELECT 
                                    ID,
                                    TRANS_ID,
                                    TRANS_ID as TRANS_ID_1,
                                    entry_time,
                                    TRANS_ID as TRANS_REF_ID,                                                    
                                    TRANS_REF_ID AS REF_ID,                                                      
                                    TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                                    BRANCH_CODE,                                                                                             
                                                                                        
                                    ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                    ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                    LCY_CODE AS TXN_CCY,   
                                    FCY_AMOUNT AMT_1,             
                                    FCY_CODE,             
                                    TRANS_CODE  AS TXN_C,                                    
                                    trans_id as TRN_REF_NO,                                    
                                    CHEQUE_NO,                           
                                    NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                                    VALUE_DATE,                
                                    BOOKING_DATE,              
                                    POSTING_DATE,              
                                    ENTRY_DATE,                
                                                    
                                    IC4_ACCOUNT_OFFICER,                 
                                    IC4_INPUTTER ,                        
                                    IC4_AUTHORISER ,                      
                                    IC4_VERIFIER  ,
                                    CHECKER_ID, 
                                    MAKER_ID,                       
                                    TEXT_FIELD_1  ,                                                      
                                    TEXT_FIELD_2, 
                                    AMT_FIELD_1,                                                     
                                    to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                                    to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                                    AMT_FIELD_2,           
                                    DATE_FIELD_1,              
                                    DATE_FIELD_2 ,             
                                    CALLOVER_REMARK,                                                                                      
                                    EXCEPTION_ID,                                                      
                                    SEVERITY_ID,                                                       
                                    REVIEW_DATE,               
                                    CALLOVER_OFFICER,                                                                                                         
                                    CALLOVER_DATE,             
                                    CALLOVER_TIME,             
                                    IC4_SPECIAL,                         
                                                                                                                            
                                    CHECKER_DATE_TIME,         
                                    CALLOVER_ID,                                                                                          
                                    POST_BRN,                                                          
                                    BATCH_NO,                                                          
                                    V_NUM,                                                             
                                    DOC_NO,               
                                    DR_TXN_NGN,             
                                    RATE,                   
                                    TXN_MNEM AS MNEM,             
                                    AC_GL_BRN_NAME,                                                    
                                    COD_BANK,             
                                    TXN_MNEMONIC AS BRN_TXN,                                                      
                                    TXN_BRANCH,                                                        
                                    AMOUNT,                 
                                    TIME_KEY AS TENOR,               
                                    TRAN_DATE ,
                                    branch_name  

                                    

                                    FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                                    WHERE  A.BRANCH_CODE = %s
                                    AND A.TRANS_ID =%s
                                    AND TRUNC(A.ENTRY_DATE)=%s
                                    AND A.CALLOVER_OFFICER IS NULL
                                    """,(request.session['selectedbranch'],list2[1],list2[2]))
                        

                        lst3=cursor14.fetchone()
                        print(lst3)
                        yList2 = dictfetchall(cursor13)
                    
                        nxt=list2[1]
                        print("d")
                        print(yList2)
                        print("e")
                        print(list2[2])
                    
                        transections = IC4_Callover_L3.objects.filter(Trans_ID=list2[1])
                        request.session['tranid'] =b_c
                        # for t in transections:
                        #     vouchers.append(t.Ref_Num)
                        #     # print("Ref_Num:", t.Ref_Num)
                        #     addresses.append(t.IP_Address)
                        #     # print("IP_Address:", t.IP_Address)
                        # voucher_id = vouchers[0]
                        # IP_Address = addresses[0]
                        return render(request, 'calloverforcontrol/acc_trans.html', {'branch_id':request.session['selectedbranch'],'prof_session':request.session['profile'],'calloverurl':request.session['calloverurl'],'nexttran':nxt,'tran':request.session['selectedbranch'],'cb':request.session['arraytest'],'results': yList2,'username':request.session['userparam'], 'trans_ID':lst3[2],'yListr':yListr,'yLists':yLists,'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
                    else:
                        return HttpResponseRedirect(reverse('calloverforcontrol_index'))
                else:
                    yList=None
                    cursor2 = connection.cursor()
                    cursor2.execute("""
                            SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
                                    SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, TO_CHAR(SUM(CREDIT), 'FM99,999,999,999,999.00') as CALL_CREDIT_TOTAL, 
                                    SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, TO_CHAR(SUM(ABS(DEBIT)), 'FM99,999,999,999,999.00') as CALL_DEBIT_TOTAL, 
                                    SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE 
                                    FROM (  SELECT TRANS_ID GRP_BY_REF,
                                    BRANCH_CODE IC4_BRANCH_CODE,
                                    ENTRY_DATE GRP_BY_DATE, 
                                    IC4_INPUTTER GRP_BY_USER, 
                                    CALLOVER_OFFICER, 
                                    case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ,
                                    case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ,
                                    case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT,
                                    case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT
                                    from (
                                    SELECT 
                                    ID,
                                    TRANS_ID,
                                    TRANS_ID as TRANS_ID_1,
                                    entry_time,
                                    TRANS_ID as TRANS_REF_ID,                                                    
                                    TRANS_REF_ID AS REF_ID,                                                      
                                    TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                                    BRANCH_CODE,                                                                                             
                                                                                        
                                    ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                    ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                    LCY_CODE AS TXN_CCY,   
                                    FCY_AMOUNT AMT_1,             
                                    FCY_CODE,             
                                    TRANS_CODE  AS TXN_C,                                    
                                    trans_id as TRN_REF_NO,                                    
                                    CHEQUE_NO,                           
                                    NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                                    VALUE_DATE,                
                                    BOOKING_DATE,              
                                    POSTING_DATE,              
                                    TO_CHAR(ENTRY_DATE, 'YYYY-MM-DD') ENTRY_DATE,                
                                                    
                                    IC4_ACCOUNT_OFFICER,                 
                                    IC4_INPUTTER ,                        
                                    IC4_AUTHORISER ,                      
                                    IC4_VERIFIER  ,
                                    CHECKER_ID, 
                                    MAKER_ID,                       
                                    TEXT_FIELD_1  ,                                                      
                                    TEXT_FIELD_2, 
                                    AMT_FIELD_1,                                                     
                                    to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                                    to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                                    AMT_FIELD_2,           
                                    DATE_FIELD_1,              
                                    DATE_FIELD_2 ,             
                                    CALLOVER_REMARK,                                                                                      
                                    EXCEPTION_ID,                                                      
                                    SEVERITY_ID,                                                       
                                    REVIEW_DATE,               
                                    CALLOVER_OFFICER,                                                                                                         
                                    CALLOVER_DATE,             
                                    CALLOVER_TIME,             
                                    IC4_SPECIAL,                         
                                                                                                                            
                                    CHECKER_DATE_TIME,         
                                    CALLOVER_ID,                                                                                          
                                    POST_BRN,                                                          
                                    BATCH_NO,                                                          
                                    V_NUM,                                                             
                                    DOC_NO,               
                                    DR_TXN_NGN,             
                                    RATE,                   
                                    TXN_MNEM AS MNEM,             
                                    AC_GL_BRN_NAME,                                                    
                                    COD_BANK,             
                                    TXN_MNEMONIC AS BRN_TXN,                                                      
                                    TXN_BRANCH,                                                        
                                    AMOUNT,                 
                                    TIME_KEY AS TENOR,               
                                    TRAN_DATE ,
                                    branch_name  

                                    FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                                    WHERE  A.BRANCH_CODE = %s
                                    AND TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD') = %s
                                    AND A.TXN_MNEMONIC='NORMAL' AND A.CALLOVER_OFFICER IS NULL
                                    AND EXISTS ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 B
                                                WHERE B.BRANCH_CODE = A.BRANCH_CODE 
                                                AND TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')
                                                AND B.TRANS_ID = A.TRANS_ID
                                                AND ABS(B.AMT_FIELD_1) >= %s
                                        )
                                    AND A.IC4_INPUTTER=%s
                                    ) a  ) a 
                                    GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                                    ORDER BY IC4_BRANCH_CODE, GRP_BY_DATE, GRP_BY_USER, GRP_BY_REF
    
                """,(request.session['selectedbranch'],request.session['transactionDate'],request.session['transLimit'],request.session['profile']))
                    list2=cursor2.fetchone()
                    if (list2):
                        cursor13 = connection.cursor()
                        useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
                                request.session['username'],
                                today_date,"""{0} re-visited the third summary page after clicking next transaction {1} and did not select any profile""".format(request.session['username'],
                                list2[1],request.session['profile']),"Callover for Control",request.session.session_key,"U-review",
                                "Callover",today,today_date)
                        cursor13.execute("""
                                        SELECT 
                                    ID,
                                    TRANS_ID,
                                    TRANS_ID as TRANS_ID_1,
                                    entry_time,
                                    TRANS_ID as TRANS_REF_ID,                                                    
                                    TRANS_REF_ID AS REF_ID,                                                      
                                    TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                                    BRANCH_CODE,                                                                                             
                                                                                        
                                    ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                    ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                    LCY_CODE AS TXN_CCY,   
                                    FCY_AMOUNT AMT_1,             
                                    FCY_CODE,             
                                    TRANS_CODE  AS TXN_C,                                    
                                    trans_id as TRN_REF_NO,                                    
                                    CHEQUE_NO,                           
                                    NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                                    VALUE_DATE,                
                                    BOOKING_DATE,              
                                    POSTING_DATE,              
                                    ENTRY_DATE,                
                                                    
                                    IC4_ACCOUNT_OFFICER,                 
                                    IC4_INPUTTER ,                        
                                    IC4_AUTHORISER ,                      
                                    IC4_VERIFIER  ,
                                    CHECKER_ID, 
                                    MAKER_ID,                       
                                    TEXT_FIELD_1  ,                                                      
                                    TEXT_FIELD_2, 
                                    AMT_FIELD_1,                                                     
                                    to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                                    to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                                    AMT_FIELD_2,           
                                    DATE_FIELD_1,              
                                    DATE_FIELD_2 ,             
                                    CALLOVER_REMARK,                                                                                      
                                    EXCEPTION_ID,                                                      
                                    SEVERITY_ID,                                                       
                                    REVIEW_DATE,               
                                    CALLOVER_OFFICER,                                                                                                         
                                    CALLOVER_DATE,             
                                    CALLOVER_TIME,             
                                    IC4_SPECIAL,                         
                                                                                                                            
                                    CHECKER_DATE_TIME,         
                                    CALLOVER_ID,                                                                                          
                                    POST_BRN,                                                          
                                    BATCH_NO,                                                          
                                    V_NUM,                                                             
                                    DOC_NO,               
                                    DR_TXN_NGN,             
                                    RATE,                   
                                    TXN_MNEM AS MNEM,             
                                    AC_GL_BRN_NAME,                                                    
                                    COD_BANK,             
                                    TXN_MNEMONIC AS BRN_TXN,                                                      
                                    TXN_BRANCH,                                                        
                                    AMOUNT,                 
                                    TIME_KEY AS TENOR,               
                                    TRAN_DATE ,
                                    branch_name  

                                    

                                    FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                                    WHERE  A.BRANCH_CODE =%s
                                    AND A.TRANS_ID =%s
                                    AND TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')=%s
                            AND A.IC4_INPUTTER = %s
                                    AND A.CALLOVER_OFFICER IS NULL
                                    """,(request.session['selectedbranch'],list2[1],list2[2],request.session['profile']))
                        
                        cursor14=connection.cursor()
                        cursor14.execute("""
                                        SELECT 
                                    ID,
                                    TRANS_ID,
                                    TRANS_ID as TRANS_ID_1,
                                    entry_time,
                                    TRANS_ID as TRANS_REF_ID,                                                    
                                    TRANS_REF_ID AS REF_ID,                                                      
                                    TRANS_SUB_ID AS TXN_SUB_ID,                                                                                                                                    
                                    BRANCH_CODE,                                                                                             
                                                                                        
                                    ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                    ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                    LCY_CODE AS TXN_CCY,   
                                    FCY_AMOUNT AMT_1,             
                                    FCY_CODE,             
                                    TRANS_CODE  AS TXN_C,                                    
                                    trans_id as TRN_REF_NO,                                    
                                    CHEQUE_NO,                           
                                    NARRATIVE AS TRANSACTION_PARTICULAR,                                                                                                                                                                                                
                                    VALUE_DATE,                
                                    BOOKING_DATE,              
                                    POSTING_DATE,              
                                    ENTRY_DATE,                
                                                    
                                    IC4_ACCOUNT_OFFICER,                 
                                    IC4_INPUTTER ,                        
                                    IC4_AUTHORISER ,                      
                                    IC4_VERIFIER  ,
                                    CHECKER_ID, 
                                    MAKER_ID,                       
                                    TEXT_FIELD_1  ,                                                      
                                    TEXT_FIELD_2, 
                                    AMT_FIELD_1,                                                     
                                    to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                                    to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT,           
                                    AMT_FIELD_2,           
                                    DATE_FIELD_1,              
                                    DATE_FIELD_2 ,             
                                    CALLOVER_REMARK,                                                                                      
                                    EXCEPTION_ID,                                                      
                                    SEVERITY_ID,                                                       
                                    REVIEW_DATE,               
                                    CALLOVER_OFFICER,                                                                                                         
                                    CALLOVER_DATE,             
                                    CALLOVER_TIME,             
                                    IC4_SPECIAL,                         
                                                                                                                            
                                    CHECKER_DATE_TIME,         
                                    CALLOVER_ID,                                                                                          
                                    POST_BRN,                                                          
                                    BATCH_NO,                                                          
                                    V_NUM,                                                             
                                    DOC_NO,               
                                    DR_TXN_NGN,             
                                    RATE,                   
                                    TXN_MNEM AS MNEM,             
                                    AC_GL_BRN_NAME,                                                    
                                    COD_BANK,             
                                    TXN_MNEMONIC AS BRN_TXN,                                                      
                                    TXN_BRANCH,                                                        
                                    AMOUNT,                 
                                    TIME_KEY AS TENOR,               
                                    TRAN_DATE ,
                                    branch_name  

                                    

                                    FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                                    WHERE  A.BRANCH_CODE = %s
                                    AND A.TRANS_ID =%s
                                    AND TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')=%s
                                    AND A.IC4_INPUTTER = %s
                                    AND A.CALLOVER_OFFICER IS NULL
                                    """,(request.session['selectedbranch'],list2[1],list2[2],request.session['profile']))
                        

                        lst3=cursor14.fetchone()
                        print(lst3)
                        yList2 = dictfetchall(cursor13)
                    
                        nxt=list2[1]
                        print("d")
                        print(yList2)
                        print("e")
                        print(list2[2])
                    
                        transections = IC4_Callover_L3.objects.filter(Trans_ID=list2[1])
                        request.session['tranid'] =b_c
                        # for t in transections:
                        #     vouchers.append(t.Ref_Num)
                        #     # print("Ref_Num:", t.Ref_Num)
                        #     addresses.append(t.IP_Address)
                        #     # print("IP_Address:", t.IP_Address)
                        # voucher_id = vouchers[0]
                        # IP_Address = addresses[0]
                        return render(request, 'calloverforcontrol/acc_trans.html', {'branch_id':request.session['selectedbranch'],'prof_session':request.session['profile'],'calloverurl':request.session['calloverurl'],'nexttran':nxt,'tran':request.session['selectedbranch'],'cb':request.session['arraytest'],'results': yList2,'username':request.session['userparam'], 'trans_ID':lst3[2],'yListr':yListr,'yLists':yLists,'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
                    else:
                        return HttpResponseRedirect(reverse('calloverforcontrol_index'))
    else:
        return HttpResponseRedirect(reverse('login'))







import json
from datetime import timedelta
from datetime import date
import numpy as np
@csrf_exempt
def Observation(request):
    
    print("Getting other details from observation model......")
   
    Selected = request.POST['selected']
    useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
                    request.session['username'],
                    today_date,"""{0} clicked on observation {1} while wanting to raise exception""".format(request.session['username'],
                    Selected),
                    "Callover for Control",request.session.session_key,"U-review","Callover",today,today_date)
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







from django.core.mail import send_mail
from datetime import datetime
from django.conf import settings
from jinja2 import Template
from datetime import timedelta
from datetime import date
@csrf_exempt
def Exceptions(request):
    request.session.set_expiry(60*25)
    transID = request.POST['transID']
    calloverDate = request.POST['calloverDate']
    reviewDate = request.POST['reviewDate']
    officer = request.POST['officer']
    observation=request.session['selected'] 
    exceptionDetails = request.POST['exceptionDetails']
    implication = request.POST['implication']
    Severity = request.POST['severity']
    useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
    request.session['username'],today_date,"""{0} raised an exception on transaction {1}""".format(request.session['username'],transID),
    "Callover for Control",request.session.session_key,"U-review","Callover",today,today_date)
    branchCode = request.POST['branchCode']
    enteryDate = request.POST['enteryDate'] 
    enteryDate2 = request.POST['enteryDate'] 
    inputterEmail = request.POST['inputterEmail']
    bsmname=request.POST['bsmheadteller']
    action = request.POST['action']
    calloverID = request.POST['calloverID']
    print('calloverID:',request.POST['bsmheadteller'])
    bsmheadteller=request.POST['bsmheadteller']
    Calloverlevel ='Callover for Control'
    Ownerdetails ='Pending Callover for Control'


    Supervisor =bsmheadteller
    reviewDate=datetime.strptime(reviewDate, '%d-%m-%Y')
    print(reviewDate)
    calloverDate=datetime.strptime(calloverDate, '%d-%m-%Y')
    print(calloverDate)
    enteryDate=datetime.strptime(enteryDate, '%d-%m-%Y')
    print(enteryDate)

    

    exception_transection = IC4_CALLOVER_EXCEPTION(CallOver_ID=calloverID, Owner_Detail=officer,Callover_Level=Calloverlevel, Branch_Code= branchCode, Maturity_Rating=transID, Inputter_Email=inputterEmail, Callover_Officer=officer, Severity_Level=Severity, Implication=implication, Action=action, Exception_Detail=exceptionDetails, Observation=observation, Issue_Priority=enteryDate, Callover_Date=calloverDate, Review=reviewDate,Supervisor=bsmheadteller,Tree_ID=5188,Exception_Status='OPEN')

    exception_transection.save()
    initialdate=request.POST.get('initialdate')
    grpbuuser=request.POST.get("txninputter")
    usrid=request.session['username']
    # transID, calloverID, severity,reviewDate,branchCode,initialdate,grpbuuser
    __update_callover2(transID, calloverID, Severity,reviewDate,branchCode,initialdate,grpbuuser,usrid)
    flag = True
    msg = "Exception Save Successfully"

    query_result = __get_config_result()
    html_content = query_result['html_text']
    cursorctotal=connection.cursor()
    call=cursorctotal.execute('''
                            SELECT BRANCH_CODE, BRANCH_NAME, ENTRY_DATE, IC4_INPUTTER, TRANS_ID, 
                                    TO_CHAR(SUM(CREDIT), 'FM99,999,999,999,999.00') AS TOTAL_CREDIT,
                                    TO_CHAR(SUM(DEBIT), 'FM99,999,999,999,999.00') AS TOTAL_DEBIT
                                    FROM (
                                    SELECT DISTINCT 
                                    T.BRANCH_CODE, 
                                    T.BRANCH_NAME, 
                                    TRUNC(T.ENTRY_DATE) ENTRY_DATE, 
                                    T.IC4_INPUTTER, 
                                    T.TRANS_ID, 
                                    T.TRANS_CODE,
                                    (CASE WHEN T.LCY_AMOUNT >=0 THEN T.LCY_AMOUNT ELSE 0 END) CREDIT,
                                    (CASE WHEN T.LCY_AMOUNT <0 THEN T.LCY_AMOUNT ELSE 0 END) DEBIT
                                    FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 T 
                                    WHERE T.TXN_MNEMONIC = 'NORMAL' 
                                    AND TRUNC(T.ENTRY_DATE) = %s
                                    AND T.TRANS_ID = %s
                                    ORDER BY TRUNC(T.ENTRY_DATE), T.BRANCH_CODE, T.IC4_INPUTTER, T.TRANS_ID
                                    )
                                    GROUP BY BRANCH_CODE, BRANCH_NAME, ENTRY_DATE, IC4_INPUTTER, TRANS_ID
     ''',(request.session['transactionDate'],transID))
    
   
    for result in call:
        branchname = result[1]
        totalcredit = result[5]
        totaldebit = result[6]
        
    # print(html_content)
    html_content2=str(html_content)
    html_content2=html_content2.replace("$ExceptionTemplate.$Reference", transID)
    html_content2=html_content2.replace("$ExceptionTemplate.$Datee",str(enteryDate2))
    html_content2=html_content2.replace("$ExceptionTemplate.$Message", exceptionDetails)
    html_content2=html_content2.replace("$ExceptionTemplate.$Implication",implication)
    html_content2=html_content2.replace("$ExceptionTemplate.$Action", action)

    html_content2=html_content2.replace("$ExceptionTemplate.$Inputter",inputterEmail)
    html_content2=html_content2.replace("$ExceptionTemplate.$Bcode", branchCode)
    html_content2=html_content2.replace("$ExceptionTemplate.$Bname", branchname)
    html_content2=html_content2.replace("$ExceptionTemplate.$Totald", totaldebit)    
    html_content2=html_content2.replace("$ExceptionTemplate.$Totalc", totalcredit) 
    html_content2=html_content2.replace("$ExceptionTemplate.$Totalc", totalcredit)
    html_content2=html_content2.replace("$ExceptionTemplate.$calloverid", calloverID)



    if(officer):
        sender_email = "adegokeadeleke.ayo@gmail.com"
        # recipient_list = [inputterEmail,bsmheadteller,myown]

        receiver_email = [inputterEmail,bsmheadteller,officer]

        password = "alvvcakmxqbfgvfa"
        message = MIMEMultipart("alternative")
     
        
        

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        # message.attach(part1)
        part2 = MIMEText(html_content2, "html")
        message.attach(part2)
        
        message.add_header("In-Reply-To",calloverID)
        message.add_header("References", calloverID)
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
    #    ch
    
        subject = 'Exception Details'
        message = MIMEMultipart("alternative")
        headers={'Reply-To':'ibukun.akinteye@adroitsolutionsltd.com'}
        message.attach(headers)
        email_from = officer
        recipient_list = ['ibukun.akinteye@adroitsolutionsltd.com','ayomide.adegoke@adroitsolutionsltd.com' ]
        password = "alvvcakmxqbfgvfa"
        message = MIMEMultipart("alternative")
        message["Subject"] = observation+" -"+calloverID
        message["From"] = officer
        message["To"] = ','.join(receiver_email)   
       
    
        
        part2 = MIMEText(html_content2, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        # message.attach(part1)
        message.attach(part2)
        myid = email.utils.make_msgid()
        request.session['mailid']=myid
        message.add_header("In-Reply-To",request.session['mailid'])
        message.add_header("References", request.session['mailid'])
        # Create secure connection with server and send email
        context = ssl.create_default_context()
        cursor=connection.cursor()
        username=cursor.execute('''SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME ='SystemMailAddress' ''')
        print(username)
        # if(officer.index("local")):
        #     officer.replace("local","com")
        #     print("officerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",officer)
        gmail_user = officer
        # to=[]
        # gmail_pwd = 'Iconcept4nbas'
        smtpserver = smtplib.SMTP("""{0}""".format(smtpserver),"""{0}""".format(smtpport))
        
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        # smtpserver.login("adegokeadeleke.ayo@gmail.com",password)
        smtpserver.sendmail(gmail_user, receiver_email,message.as_string())
        print(">>>>>>>>>>>>>>>>>>>   success")
        # with smtplib.SMTP_SSL('''{0}'''.format(smtpserver), '''{0}'''.format(smtpport), context=context) as server:
        #     server.login(username, password)
        #     server.sendmail(
        #         sender_email, receiver_email, message.as_string()
        #     )


        # subject = 'Exception Details'
        # message=''
        
        # email_from = officer
        # recipient_list = [inputterEmail,bsmheadteller,myown]
        # send_mail(subject, message, email_from, recipient_list, fail_silently=False,html_message=html_content2)

    args = {           
            'flag': flag,
            'msg': msg,
                    
        }
    return JsonResponse(args)


# @staff_member_required
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
def __update_callover2(transID, calloverID, severity,reviewDate,branchCode,initialdate,grpbuuser,usrid):
        #    __update_callover(id,  my_id, today, todaye,username,branchCode,initialdate,grpbuuser)
    cursor=connection.cursor()

    cursor.execute(''' 
                UPDATE CALLOVER_TRANSACTION_L3

                    SET CALLOVER_DATE = %s, 
                    
                    CALLOVER_ID = %s, 
                    CALLOVER_TIME=%s,
                    CALLOVER_OFFICER = %s,
                    SEVERITY_ID = %s,
                    EXCEPTION_ID = %s
                    WHERE TRUNC(ENTRY_DATE) = %s
                    AND TRANS_ID = %s
                    AND BRANCH_CODE = %s
                    AND IC4_INPUTTER = %s
                 ''',(today,calloverID,date_time,usrid,severity,calloverID,initialdate,transID,branchCode,grpbuuser))
                #  .format(reviewDate,severity,calloverID,initialdate,transID,branchCode,grpbuuser,usrid,date_time,today))
                # calldate=date_time,calloverid=self,caltime=datetime,callofficer=usrid,severity=severity,exceptionid=calloverid,
                # entrydate=initialdate,transid=transId
    cursor.execute('''commit''')
    print("did thissssssssssssssssssssssssss")
 
def __get_config_result():
    query = comfig_query()
    cursor = connection.cursor()
    results = cursor.execute(query)
    for result in results:
        html_text = result[0]
       
    Dict =dict()
    Dict['html_text'] = html_text
    
    return Dict

def __get_query_result(trasn_id):
    print('>>>>>>>>>>>>>>>>>>',trasn_id)
    
    cursor = connection.cursor()
    results = cursor.execute('''SELECT IC4_BRANCH_CODE, TRANS_ID_1, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, TXN_CODE, 
                    SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, 
                    SUM(CREDIT) CALL_CREDIT_TOTAL, SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, SUM(ABS(DEBIT)) as CALL_DEBIT_TOTAL, 
                    SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE FROM ( SELECT "TRANS_ID_1" TRANS_ID_1, "TRANS_ID" GRP_BY_REF, 
                    "TXN_CODE" TXN_CODE, "BRANCH_CODE" IC4_BRANCH_CODE, "ENTRY_DATE" GRP_BY_DATE, 
                    "IC4_INPUTTER" GRP_BY_USER, CALLOVER_OFFICER, 
                    case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ, case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ, 
                    case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT, case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT 
                    from ( 
                    SELECT ID, 
                     TRANS_ID, TRANS_ID AS TRANS_ID_1,
                    TRANS_REF_ID, TRANS_REF_ID AS REF_ID, TRANS_SUB_ID AS TXN_SUB_ID, 
                    BRANCH_CODE, BRANCH_NAME, ACCOUNT_ID AS ACCOUNT_NUMBER, ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME , 
                    LCY_CODE, to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT,
                    to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT, FCY_CODE, TRANS_CODE  AS TXN_C, TRANS_ID as TRN_REF_NO, CHEQUE_NO, 
                    NARRATIVE AS TRANSACTION_PARTICULAR, ENTRY_DATE AS VALUE_DATE, TRAN_DATE, BOOKING_DATE, 
                    POSTING_DATE, ENTRY_DATE, ENTRY_TIME, IC4_ACCOUNT_OFFICER, IC4_INPUTTER , IC4_AUTHORISER , 
                    IC4_VERIFIER  , CHECKER_ID, MAKER_ID, TEXT_FIELD_1  , TEXT_FIELD_2, AMT_FIELD_1, AMT_FIELD_2, 
                    DATE_FIELD_1, DATE_FIELD_2 , CALLOVER_REMARK, EXCEPTION_ID, SEVERITY_ID, REVIEW_DATE, 
                    CALLOVER_OFFICER, CALLOVER_DATE, CALLOVER_TIME, IC4_SPECIAL, CHECKER_DATE_TIME, CALLOVER_ID, 
                    POST_BRN, BATCH_NO, V_NUM, DOC_NO, DR_TXN_NGN, RATE, TXN_MNEM AS MNEM, AC_GL_BRN_NAME, COD_BANK, 
                    TXN_MNEMONIC, TXN_BRANCH, AMOUNT, TXN_CODE,TIME_KEY AS TENOR, REF_NUM 
                    FROM CALLOVER_TRANSACTION_L3 A
                    WHERE  A.TRANS_ID = %(transid)s
                    AND A.TXN_MNEMONIC = 'NORMAL'

                    ) a ) a GROUP BY IC4_BRANCH_CODE, TRANS_ID_1, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, TXN_CODE''',{'transid':trasn_id})
    
    for result in results:
        branch = result[0]
        trans_id = result[1]
        date = result[3]
        officer = result[4]
        user = result[5]
        TXN_CODE = result[6]
        trans_id_1 = result[6]
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
    Dict['trans_id_1']=trans_id_1
    
    return Dict

def update_trans(request):
    if request.is_ajax and request.method == "POST":
        id = request.POST['id']
        transection = IC4_Callover_L3.objects.get(pk=id)


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
                UPDATE CALLOVER_TRANSACTION_L3
            SET CALLOVER_DATE = %s, 
            CALLOVER_TIME = %s,
            CALLOVER_ID = %s, 
            CALLOVER_OFFICER = %s
            WHERE TRUNC(ENTRY_DATE) = %s
            AND TRANS_ID = %s
            AND BRANCH_CODE = %s
            AND IC4_INPUTTER = %s
                 ''',(date,time,callover_id,username,initialdate,trans_id,branchCode,grpbuuser))
    cursor.execute('''commit''')


import json
from datetime import timedelta
from datetime import date
import numpy as np
@csrf_exempt
def OCR(request):
    request.session.set_expiry(60*5)
    print("=====================================================")
    print(request.POST['status'])
    username=request.session['username']
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


        if(request.POST.get('exclude')):
            print("exclude")
        else:
            branchCode=query_result['branch']
            initialdate=query_result['date']
            grpbuuser=query_result['user']
            __update_callover(id,  my_id, today, todaye,username,branchCode,initialdate,grpbuuser)
            
            useractivity(request.session.session_key,"Callover for Control",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
                    request.session['username'],
                    today_date,"""{0} called over transaction {1}""".format(request.session['username'],query_result['trans_id']),
                    "Callover for Control",request.session.session_key,"U-review","Callover",today,today_date)


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


    # if (status=="False"):
    #     accepted_transection = IC4_ACCEPTED_CALLOVER(CallOver_ID=callover_ID,
    #                                                  GRP_BY_REF=query_result['trans_id'],
    #                                                  GRP_BY_USER=query_result['user'],
    #                                                  GRP_BY_DATE=query_result['date'],
    #                                                  Branch_Code=query_result['branch'],
    #                                                  Ref_Num=voucher)
    #     accepted_transection.save()
    #     __update_callover(id, callover_ID, today, current_time)
    #     flag = True
    #     args = {
    #         'flag': flag,
    #     }

    return JsonResponse(args)






