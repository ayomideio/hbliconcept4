from io import BytesIO


import requests
import time

from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.http import HttpResponseRedirect,HttpResponse,HttpResponseRedirect,JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import pandas as pd
from pendingcalloverforcontrol.models import IC4_ACCEPTED_CALLOVER
from iconcept4.models import IC4_CALLOVER_EXCEPTION,Profile,IC4_Observation_Model,IC4_Callover_L3
from .queries import *
from django.db import connection
from django.urls import reverse
import socket
from iconcept4.views import useractivity
from datetime import datetime
today=datetime.date(datetime.now())
date_time=datetime.now()
from iconcept4.views import dictfetchall
from iconcept4.views import returnallbranch

def index(request):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):
        b_c = ''
        transLimit=request.POST.get('transLimit')
        request.session['transLimit']=0
        
        if (transLimit is not  None):
    
            request.session['transLimit']=transLimit
        if('transLimit' in request.session):
            b_c = ''
            username=request.session['userparam']
            pbranch=request.session['secondarybranch']
            today_date = '19-JUL-18'
            

            b_c=returnallbranch(request.session['secondarybranch'],request.session['username'])
            print(b_c)
            cursor = connection.cursor()
            useractivity(request.session.session_key,"Callover for Control Special",socket.gethostbyname(socket.gethostname()),socket.gethostname(),request.session['username'],
                                    today_date,"""{0} visited the first summary page""".format(request.session['username']),"Callover for Control Special",request.session.session_key,"U-review",
                                        "Callover",today,today_date)
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
                                                (A.BRANCH_CODE || SUBSTR(TRANS_SUB_ID,1,7))trans_id_1,
                                                TRANS_ID as TRANS_ID,
                                                entry_time,
                                                TRANS_ID as TRANS_REF_ID,                                                    
                                                TRANS_REF_ID AS REF_ID,                                                      
                                                TRANS_SUB_ID AS AC_ENTRY_SR_NO,                                                                                                                                    
                                                BRANCH_CODE,                                                                                             
                                                                                                    
                                                ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                                ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                                LCY_CODE AS TXN_CCY,   
                                                FCY_AMOUNT AMT_1,             
                                                FCY_CODE,             
                                                TRANS_CODE  AS DRCR,                                    
                                                trans_id as TRN_REF_NO,                                    
                                                CHEQUE_NO,                           
                                                NARRATIVE AS TRANSACTION_NARRATIVE,                                                                                                                                                                                                
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
                                                TIME_KEY,               
                                                TRAN_DATE ,
                                                branch_name  

                                                

                                                FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                                                WHERE A.BRANCH_CODE IN ({0})
                                                AND A.CALLOVER_OFFICER IS NULL
                                                AND A.TXN_MNEMONIC='NORMAL'
                                                AND A.CALLOVER_OFFICER IS NULL
                                                AND EXISTS ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 B
                                                        WHERE  B.BRANCH_CODE = A.BRANCH_CODE 
                                                        AND TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')
                                                        AND B.TRANS_ID = A.TRANS_ID
                                                        AND ABS(B.AMT_FIELD_1) >= %(limit)s
                                                        AND B.CALLOVER_OFFICER IS NULL 
                                                )    
                                                ) a  ) a 
                                                GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                                                ) GROUP BY GRP_BY_DATE, IC4_BRANCH_CODE
                                                ORDER BY GRP_BY_DATE, IC4_BRANCH_CODE

                                                    '''.format(b_c),{'limit':request.session['transLimit']})

            yList = dictfetchall(cursor)
        
            columns = [col[0] for col in cursor.description]
            # print(yList)
            # profiles = IC4_Profile.objects.all()

            profiles = Profile.objects.all()
        
            return render(request, 'calloverforcontrolspecial/library.html', {'results':yList,'transLimit':request.session['transLimit'], 'Profiles':profiles, 'test':'branch_cd','username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
    else:
        return HttpResponseRedirect(reverse('login'))



# @staff_member_required
def Bank_Trans(request, branch_id):
    request.session.set_expiry(60*5)
    if('userparam' in request.session):
        transactionDate=request.POST.get('dateVal')
        request.session['transactionDate']=transactionDate
        request.session['arraytest']=""
        query = trans_query(branch_id)
        cursor = connection.cursor()
        useractivity(request.session.session_key,"Callover for Control Special",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
            request.session['username'],
            today_date,"""{0} visited the second summary page after clicking on branch {1} from the first summary page""".format(request.session['username'],
            branch_id),"Callover for Control Special",request.session.session_key,"U-review",
            "Callover",today,today_date)
        result = cursor.execute("""
                    SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
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
                                    (A.BRANCH_CODE || SUBSTR(TRANS_SUB_ID,1,7))trans_id_1,
                                    TRANS_ID as TRANS_ID,
                                    entry_time,
                                    TRANS_ID as TRANS_REF_ID,                                                    
                                    TRANS_REF_ID AS REF_ID,                                                      
                                    TRANS_SUB_ID AS AC_ENTRY_SR_NO,                                                                                                                                    
                                    BRANCH_CODE,                                                                                             
                                                                                        
                                    ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                    ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                    LCY_CODE AS TXN_CCY,   
                                    FCY_AMOUNT AMT_1,             
                                    FCY_CODE,             
                                    TRANS_CODE  AS DRCR,                                    
                                    trans_id as TRN_REF_NO,                                    
                                    CHEQUE_NO,                           
                                    NARRATIVE AS TRANSACTION_NARRATIVE,                                                                                                                                                                                                
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
                                    TIME_KEY,               
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
                                    GROUP BY IC4_BRANCH_CODE, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                                    ORDER BY GRP_BY_DATE, IC4_BRANCH_CODE, GRP_BY_USER

                                        """,(branch_id,request.session['transactionDate'],request.session['transLimit']))
        request.session['selectedbranch'] =branch_id
        
        yList = dictfetchall(cursor)
        request.session['arraytest']=""
        # request.session['arraytest']=[{'IC4_BRANCH_CODE': '010', 'GRP_BY_REF': '010CHDP182000006', 'CALLOVER_OFFICER': None, 'GRP_BY_USER': 'CHIAMAECHI', 'CALL_NO_OF_VOUCHERS': 2, 'CALL_CREDIT_FREQ': 1, 'CALL_CREDIT_TOTAL': 2300, 'CALL_DEBIT_FREQ': 1, 'CALL_DEBIT_TOTAL': 2300, 'CALL_DIFFERENCE': 0}, {'IC4_BRANCH_CODE': '010', 'GRP_BY_REF': '010CHDP182000515',  'CALLOVER_OFFICER': None, 'GRP_BY_USER': 'FCAGU', 'CALL_NO_OF_VOUCHERS': 2, 'CALL_CREDIT_FREQ': 1, 'CALL_CREDIT_TOTAL': 4000, 'CALL_DEBIT_FREQ': 1, 'CALL_DEBIT_TOTAL': 4000, 'CALL_DIFFERENCE': 0}]
        # print(yList)

        return render(request, 'calloverforcontrolspecial/branch_trans.html', {'results': yList,'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
    else:
        return HttpResponseRedirect(reverse('login'))



# @staff_member_required
def Profile_Trans(request, Profile_ID):
    query = trans_query_profiles(Profile_ID)
    cursor = connection.cursor()
    result = cursor.execute(query, None)
    ylist=dictfetchall(cursor)

    return render(request, 'callover/branch_trans.html', {'results': ylist})

# @staff_member_required
def acc_trans(request, trans_id):
    # request.session['arraytest'].pop(0)
    # print(request.session['arraytest'])
    request.session.set_expiry(60*5)
    if('userparam' in request.session):

        b_c = '010'
        today_date = '2018-07-19'
        trans_id = trans_id.strip()
        # br_nc=branch.strip
        # print('branch:',br_nc)
        tst=request.POST.get('vala')
        # tst = '2018-07-19'
        # print(tst)
        # print(tst)
        # print("Tran_id:",trans_id)
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
        SELECT USER_ID, FIRST_NAME FROM IC4_PRO_USERS lst WHERE BRANCH_CODE = %(branchcode)s AND USER_ROLE IN('BSM', 'HEADTELLER')
        """,{'branchcode':request.session['selectedbranch']})
        yLists = dictfetchall(resultss)


        query = acc_query(trans_id)
        cursor = connection.cursor()
        useractivity(request.session.session_key,"Callover for Control Special",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
            request.session['username'],
            today_date,"""{0} visited the third summary page after clicking on transaction id {1} from the second summary page""".format(request.session['username'],
            trans_id),"Callover for Control Special",request.session.session_key,"U-review",
            "Callover",today,today_date)
        results = cursor.execute("""
                                    SELECT 
                                                ID,
                                                (A.BRANCH_CODE || SUBSTR(TRANS_SUB_ID,1,7))trans_id_1,
                                                TRANS_ID as TRANS_ID,
                                                entry_time,
                                                TRANS_ID as TRANS_REF_ID,                                                    
                                                TRANS_REF_ID AS REF_ID,                                                      
                                                TRANS_SUB_ID AS AC_ENTRY_SR_NO,                                                                                                                                    
                                                BRANCH_CODE,                                                                                             
                                                                                                    
                                                ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                                ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                                LCY_CODE AS TXN_CCY,   
                                                FCY_AMOUNT AMT_1,             
                                                FCY_CODE,             
                                                TRANS_CODE  AS DRCR,                                    
                                                trans_id as TRN_REF_NO,                                    
                                                CHEQUE_NO,                           
                                                NARRATIVE AS TRANSACTION_NARRATIVE,                                                                                                                                                                                                
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
                                                TIME_KEY,               
                                                TRAN_DATE ,
                                                branch_name  

                                                

                                                FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                                                WHERE  A.BRANCH_CODE =%s
                                                AND A.IC4_INPUTTER=%s
                                                AND A.ENTRY_DATE= %s
                                                AND A.TXN_MNEMONIC='NORMAL' 
                                                AND A.CALLOVER_OFFICER IS NULL
                                                AND EXISTS ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 B
                                                    WHERE  B.BRANCH_CODE = A.BRANCH_CODE 
                                                    AND TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')
                                                    AND B.TRANS_ID = A.TRANS_ID
                                                    AND B.CALLOVER_OFFICER IS NULL 
                                                    AND ABS(B.AMT_FIELD_1) >= %s

                                                    )


                                    """,(request.session['selectedbranch'] ,trans_id,request.session['transactionDate'],request.session['transLimit']))
        request.session['currentInputter']=trans_id
        yList = dictfetchall(results)
        print("a")
        # print(yList)
        print("b")
        if (yList):
    
            tst=""" date={1}  data2={0} """.format(trans_id,today_date)
            # print(tst)
            # print("yList:",yList)
            transections = IC4_Callover_L3.objects.filter(IC4_Inputter=trans_id)
            request.session['tranid'] =b_c
            for t in transections:
                vouchers.append(t.Ref_Num)
                # print("Ref_Num:", t.Ref_Num)
                addresses.append(t.IP_Address)
                # print("IP_Address:", t.IP_Address)
            voucher_id = vouchers[0]
            IP_Address = addresses[0]
            return render(request, 'calloverforcontrolspecial/acc_trans.html', {'tran':request.session['selectedbranch'],'cb':request.session['arraytest'],'results': yList,'username':request.session['userparam'], 'voucher_id':voucher_id, 'IP_Address':IP_Address, 'trans_ID':trans_id,'yListr':yListr,'yLists':yLists,'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
        else:
            yList=None
            print("Noner")
            cursor2 = connection.cursor()
            cursor2.execute("""         SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
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
                                        (A.BRANCH_CODE || SUBSTR(TRANS_SUB_ID,1,7))trans_id_1,
                                        TRANS_ID as TRANS_ID,
                                        entry_time,
                                        TRANS_ID as TRANS_REF_ID,                                                    
                                        TRANS_REF_ID AS REF_ID,                                                      
                                        TRANS_SUB_ID AS AC_ENTRY_SR_NO,                                                                                                                                    
                                        BRANCH_CODE,                                                                                             
                                                                                            
                                        ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                        ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                        LCY_CODE AS TXN_CCY,   
                                        FCY_AMOUNT AMT_1,             
                                        FCY_CODE,             
                                        TRANS_CODE  AS DRCR,                                    
                                        trans_id as TRN_REF_NO,                                    
                                        CHEQUE_NO,                           
                                        NARRATIVE AS TRANSACTION_NARRATIVE,                                                                                                                                                                                                
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
                                        TIME_KEY,               
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
                                        GROUP BY IC4_BRANCH_CODE, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                                        ORDER BY GRP_BY_DATE, IC4_BRANCH_CODE, GRP_BY_USER

                                            """,(request.session['selectedbranch'],request.session['transactionDate'],request.session['transLimit']))
            list2=cursor2.fetchone()
            if(list2):
                print("list 2  of 2")
                print(list2)
                print(list2[1])
                cursor13 = connection.cursor()
                useractivity(request.session.session_key,"Callover for Control Special",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
                                request.session['username'],
                                today_date,"""{0} re-visited the third summary page after clicking next transaction {1} and did not select any profile""".format(request.session['username'],
                                list2[1],request.session['profile']),"Callover for Control Special",request.session.session_key,"U-review",
                                "Callover",today,today_date)
                cursor13.execute("""
                                    SELECT 
                                        ID,
                                        (A.BRANCH_CODE || SUBSTR(TRANS_SUB_ID,1,7))trans_id_1,
                                        TRANS_ID as TRANS_ID,
                                        entry_time,
                                        TRANS_ID as TRANS_REF_ID,                                                    
                                        TRANS_REF_ID AS REF_ID,                                                      
                                        TRANS_SUB_ID AS AC_ENTRY_SR_NO,                                                                                                                                    
                                        BRANCH_CODE,                                                                                             
                                                                                            
                                        ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
                                        ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
                                        LCY_CODE AS TXN_CCY,   
                                        FCY_AMOUNT AMT_1,             
                                        FCY_CODE,             
                                        TRANS_CODE  AS DRCR,                                    
                                        trans_id as TRN_REF_NO,                                    
                                        CHEQUE_NO,                           
                                        NARRATIVE AS TRANSACTION_NARRATIVE,                                                                                                                                                                                                
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
                                        TIME_KEY,               
                                        TRAN_DATE ,
                                        branch_name  

                                        

                                        FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 A
                                        WHERE  A.BRANCH_CODE = %s

                                        AND A.IC4_INPUTTER=%s
                                        AND A.ENTRY_DATE= %s
                                        AND A.CALLOVER_OFFICER IS NULL
                                        AND A.TXN_MNEMONIC='NORMAL'
                                        AND EXISTS ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 B
                                            WHERE  B.BRANCH_CODE = A.BRANCH_CODE 
                                            AND TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')
                                            AND B.TRANS_ID = A.TRANS_ID
                                            AND ABS(B.LCY_AMOUNT) >= %s
                                            AND B.CALLOVER_OFFICER IS NULL 
                                        )

                                        """,(request.session['selectedbranch'],list2[3],list2[1],request.session['transLimit']))
                yList2 = dictfetchall(cursor13)
                nxt=list2[3]
                print("d")
                print(yList2)
                print("e")
                print(list2[2])
            
                transections = IC4_Callover_L3.objects.filter(IC4_Inputter=list2[3])
                request.session['tranid'] =b_c
                for t in transections:
                    vouchers.append(t.Ref_Num)
                    # print("Ref_Num:", t.Ref_Num)
                    addresses.append(t.IP_Address)
                    # print("IP_Address:", t.IP_Address)
                voucher_id = vouchers[0]
                IP_Address = addresses[0]
                return render(request, 'calloverforcontrolspecial/acc_trans.html', {'nexttran':nxt,'tran':request.session['selectedbranch'],'cb':request.session['arraytest'],'results': yList2,'username':request.session['userparam'], 'voucher_id':voucher_id, 'IP_Address':IP_Address, 'trans_ID':list2[1],'yListr':yListr,'yLists':yLists,'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
            else:
                return HttpResponseRedirect(reverse('calloverforcontrolspecial_index'))    

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
    useractivity(request.session.session_key,"Callover for Control Special",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
                    request.session['username'],
                    today_date,"""{0} clicked on observation {1} while wanting to raise exception""".format(request.session['username'],
                    Selected),
                    "Callover for Control Special",request.session.session_key,"U-review","Callover",today,today_date)
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
    
    transID = request.POST['transID']
    print(transID)
    calloverDate = request.POST['calloverDate']
    reviewDate = request.POST['reviewDate']
    # officer = request.POST['officer']
    # print('officer:'+officer)
    observation = request.POST['observation']
    exceptionDetails = request.POST['exceptionDetails']
    implication = request.POST['implication']
    Severity = request.POST['severity']
    branchCode = request.POST['branchCode']
    enteryDate = request.POST['enteryDate'] 
    enteryDate2 = request.POST['enteryDate'] 
    inputterEmail2 = request.POST['inputterEmail']
    # print('inputterEmail:'+inputterEmail)
    action = request.POST['action']
    calloverID = request.POST['calloverID']
    # bsmheadteller=request.POST['bsmheadtelle']
    # print('inputterEmail:'+bsmheadteller)
    Calloverlevel ='Callover for Tellers'
    Ownerdetails ='Pending Callover for Tellers'

    # for Test
    officer='ademola.oa@gmail.com'
    bsmheadteller='oseni.titiloye@adroitconsultingltd.com'
    inputterEmail='ibukun.akinteye@adroitsolutionsltd.com'
    myown='olufemi.ademola@adroitsolutionsltd.com'

    Supervisor =bsmheadteller
    reviewDate=datetime.strptime(reviewDate, '%d-%m-%Y')
    print(reviewDate)
    calloverDate=datetime.strptime(calloverDate, '%d-%m-%Y')
    print(calloverDate)
    enteryDate=datetime.strptime(enteryDate, '%d-%m-%Y')
    print(enteryDate)

    exception_transection = IC4_CALLOVER_EXCEPTION(CallOver_ID=calloverID, Owner_Details=Ownerdetails,Callover_Level=Calloverlevel, Branch_Code= branchCode, Trans_ID=transID, IC4_Inputter=inputterEmail, Callover_Officer=officer, Severity_Level=Severity, Implication=implication, Action=action, Exception_Details=exceptionDetails, Observation=observation, Entery_Date=enteryDate, Callover_Date=calloverDate, Review=reviewDate,Supervisor=bsmheadteller)

    exception_transection.save()
    __update_callover2(transID, calloverID, Severity,reviewDate)
    flag = True
    msg = "Exception Save Successfully"

    query_result = __get_config_result()
    html_content = query_result['html_text']
    print(html_content)
    html_content2=str(html_content)
    print(html_content2)

    html_content2=html_content2.replace("$ExceptionTemplate.$Reference", transID)
    html_content2=html_content2.replace("$ExceptionTemplate.$Datee",str(enteryDate2))
    html_content2=html_content2.replace("$ExceptionTemplate.$Severity", Severity)
    html_content2=html_content2.replace("$ExceptionTemplate.$Message", exceptionDetails)
    html_content2=html_content2.replace("$ExceptionTemplate.$Implication",implication)
    html_content2=html_content2.replace("$ExceptionTemplate.$Action", action)

    html_content2=html_content2.replace("$ExceptionTemplate.$Inputter",inputterEmail2)
    html_content2=html_content2.replace("$ExceptionTemplate.$Bcode", branchCode)
        

    if(officer):
        subject = 'Exception Details'
        message=''
        
        email_from = officer
        recipient_list = [inputterEmail,bsmheadteller,myown]
        send_mail(subject, message, email_from, recipient_list, fail_silently=False,html_message=html_content2)

    args = {           
            'flag': flag,
            'msg': msg,
                    
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
def __update_callover2(transID, calloverID, severity,reviewDate):
   
    transections = IC4_Callover_L3.objects.filter(Trans_ID=transID)
    for transection in transections:
        transection.Exception_Id = calloverID
        transection.Severity_Id = severity
        transection.Review_Date = reviewDate
        transection.save()

def __get_config_result():
    query = comfig_query()
    cursor = connection.cursor()
    results = cursor.execute(query)
    for result in results:
        html_text = result[0]
       
    Dict =dict()
    Dict['html_text'] = html_text
    
    return Dict

def __get_query_result(trasn_id,date):
    query = '''
    SELECT IC4_BRANCH_CODE, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, TXN_CODE,
SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, SUM(CREDIT) CALL_CREDIT_TOTAL,
SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, SUM(ABS(DEBIT)) as CALL_DEBIT_TOTAL, SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE FROM
( SELECT "TRANS_ID" GRP_BY_REF, "TXN_CODE" TXN_CODE, "BRANCH_CODE" IC4_BRANCH_CODE, "ENTRY_DATE" GRP_BY_DATE, "IC4_INPUTTER" 
GRP_BY_USER, CALLOVER_OFFICER, case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ, case when "AMT_FIELD_1" 
<0 then 1 else 0 end as DEBIT_FREQ, case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT, case when "AMT_FIELD_1" 
<0 then "AMT_FIELD_1" else 0 end as DEBIT from ( SELECT ID, trans_id, TRANS_REF_ID, TRANS_REF_ID AS REF_ID, TRANS_SUB_ID AS AC_ENTRY_SR_NO, 
BRANCH_CODE, BRANCH_NAME, ACCOUNT_ID AS ACCOUNT_NUMBER, ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME , LCY_CODE, 
to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT, to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT, FCY_CODE, TRANS_CODE AS TXN_C, 
TRANS_MODE as TRN_REF_NO, CHEQUE_NO, NARRATIVE AS TRANSACTION_NARRATIVE, ENTRY_DATE AS VALUE_DATE, TRAN_DATE, BOOKING_DATE, POSTING_DATE, 
ENTRY_DATE, ENTRY_TIME, IC4_ACCOUNT_OFFICER, IC4_INPUTTER , IC4_AUTHORISER , IC4_VERIFIER  , CHECKER_ID, MAKER_ID, TEXT_FIELD_1  , TEXT_FIELD_2, 
AMT_FIELD_1, AMT_FIELD_2, DATE_FIELD_1, DATE_FIELD_2 , CALLOVER_REMARK, EXCEPTION_ID, SEVERITY_ID, REVIEW_DATE, CALLOVER_OFFICER, CALLOVER_DATE, 
CALLOVER_TIME, IC4_SPECIAL, CHECKER_DATE_TIME, CALLOVER_ID, POST_BRN, BATCH_NO, V_NUM, DOC_NO, DR_TXN_NGN, RATE, TXN_MNEM AS MNEM, AC_GL_BRN_NAME, 
COD_BANK, TXN_MNEMONIC, TXN_BRANCH, AMOUNT, TXN_CODE,TIME_KEY, REF_NUM FROM callover_transaction_l3 WHERE  
ic4_inputter = '{0}'  AND TO_CHAR(ENTRY_DATE, 'YYYY-MM-DD') = '{1}'
 ) a ) a GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, 
GRP_BY_USER, TXN_CODE
    '''.format(trasn_id,date)
    cursor = connection.cursor()
    results = cursor.execute('''
        SELECT IC4_BRANCH_CODE, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, TXN_CODE,
                        SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, SUM(CREDIT) CALL_CREDIT_TOTAL,
                        SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, SUM(ABS(DEBIT)) as CALL_DEBIT_TOTAL, SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE FROM
                        ( SELECT "TRANS_ID" GRP_BY_REF, "TXN_CODE" TXN_CODE, "BRANCH_CODE" IC4_BRANCH_CODE, "ENTRY_DATE" GRP_BY_DATE, "IC4_INPUTTER" 
                        GRP_BY_USER, CALLOVER_OFFICER, case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ, case when "AMT_FIELD_1" 
                        <0 then 1 else 0 end as DEBIT_FREQ, case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT, case when "AMT_FIELD_1" 
                        <0 then "AMT_FIELD_1" else 0 end as DEBIT from ( SELECT ID, trans_id, TRANS_REF_ID, TRANS_REF_ID AS REF_ID, TRANS_SUB_ID AS AC_ENTRY_SR_NO, 
                        BRANCH_CODE, BRANCH_NAME, ACCOUNT_ID AS ACCOUNT_NUMBER, ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME , LCY_CODE, 
                        to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00') LCY_AMOUNT, to_char(AMT_FIELD_2, 'FM99,999,999,999,999.00') FCY_AMOUNT, FCY_CODE, TRANS_CODE AS TXN_C, 
                        TRANS_MODE as TRN_REF_NO, CHEQUE_NO, NARRATIVE AS TRANSACTION_NARRATIVE, ENTRY_DATE AS VALUE_DATE, TRAN_DATE, BOOKING_DATE, POSTING_DATE, 
                        ENTRY_DATE, ENTRY_TIME, IC4_ACCOUNT_OFFICER, IC4_INPUTTER , IC4_AUTHORISER , IC4_VERIFIER  , CHECKER_ID, MAKER_ID, TEXT_FIELD_1  , TEXT_FIELD_2, 
                        AMT_FIELD_1, AMT_FIELD_2, DATE_FIELD_1, DATE_FIELD_2 , CALLOVER_REMARK, EXCEPTION_ID, SEVERITY_ID, REVIEW_DATE, CALLOVER_OFFICER, CALLOVER_DATE, 
                        CALLOVER_TIME, IC4_SPECIAL, CHECKER_DATE_TIME, CALLOVER_ID, POST_BRN, BATCH_NO, V_NUM, DOC_NO, DR_TXN_NGN, RATE, TXN_MNEM AS MNEM, AC_GL_BRN_NAME, 
                        COD_BANK, TXN_MNEMONIC, TXN_BRANCH, AMOUNT, TXN_CODE,TIME_KEY, REF_NUM FROM callover_transaction_l3 WHERE  
                        ic4_inputter = %s  AND TO_CHAR(ENTRY_DATE, 'YYYY-MM-DD') = %s
                        ) a ) a GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, 
                        GRP_BY_USER, TXN_CODE
                            ''',(trasn_id,date))
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

def __update_callover(trans_id,callover_id,date, time, username):
   
    transections = IC4_Callover_L3.objects.filter(IC4_Inputter=trans_id)
    for transection in transections:
        transection.Callover_ID = callover_id
        transection.Callover_Officer = username
        transection.Callover_Date = date
        transection.Callover_Time = time
        transection.save()
        accepted_transection = IC4_ACCEPTED_CALLOVER(CallOver_ID=my_id,
                                                                         GRP_BY_REF=query_result['trans_id'],
                                                                         GRP_BY_USER=query_result['user'],
                                                                         GRP_BY_DATE=query_result['date'],
                                                                         Branch_Code=query_result['branch'],
                                                                         Callover_Officer=username,
                                                                         Tree_Key=5188,
                                                                         Ref_Num=voucher)
        accepted_transection.save()

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
    todayd=todayd.strftime("%Y-%m-%d")
    todaye=time.strftime("%Y-%m-%d %H:%M:%S", t)

    addt='000'
    current_tim = time.strftime("%H%M", t)
    current_tim2=current_tim+addt
    flag = False
    id = request.POST['id']
    print('idddddddddddddddddddddd>>>>>>>>>>>>>>>>>>>>>>>>>>',id)
    # pdf = request.POST['pdf']
    voucher = request.POST['voucher']
    status = request.POST['status']
    
    initialcursor=connection.cursor()
    initialcursor.execute(''' 
                                SELECT IC4_BRANCH_CODE, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, TXN_CODE,
                                    SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, SUM(CREDIT) CALL_CREDIT_TOTAL,
                                    SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, SUM(ABS(DEBIT)) as CALL_DEBIT_TOTAL, SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE FROM
                                    ( SELECT "TRANS_ID" GRP_BY_REF, "TXN_CODE" TXN_CODE, "BRANCH_CODE" IC4_BRANCH_CODE, "ENTRY_DATE" GRP_BY_DATE, "IC4_INPUTTER" 
                                    GRP_BY_USER, CALLOVER_OFFICER, case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ, case when "AMT_FIELD_1" 
                                    <0 then 1 else 0 end as DEBIT_FREQ, case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT, case when "AMT_FIELD_1" 
                                    <0 then "AMT_FIELD_1" else 0 end as DEBIT from ( SELECT ID, trans_id, TRANS_REF_ID, TRANS_REF_ID AS REF_ID, TRANS_SUB_ID AS AC_ENTRY_SR_NO, 
                                    BRANCH_CODE, BRANCH_NAME, ACCOUNT_ID AS ACCOUNT_NUMBER, ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME , LCY_CODE, FCY_AMOUNT, FCY_CODE, TRANS_CODE  
                                    AS TXN_C, TRANS_MODE as TRN_REF_NO, CHEQUE_NO, NARRATIVE AS TRANSACTION_NARRATIVE, ENTRY_DATE AS VALUE_DATE, TRAN_DATE, BOOKING_DATE, POSTING_DATE, 
                                    ENTRY_DATE, ENTRY_TIME, IC4_ACCOUNT_OFFICER, IC4_INPUTTER , IC4_AUTHORISER , IC4_VERIFIER  , CHECKER_ID, MAKER_ID, TEXT_FIELD_1  , TEXT_FIELD_2, 
                                    AMT_FIELD_1, AMT_FIELD_2, DATE_FIELD_1, DATE_FIELD_2 , CALLOVER_REMARK, EXCEPTION_ID, SEVERITY_ID, REVIEW_DATE, CALLOVER_OFFICER, CALLOVER_DATE, 
                                    CALLOVER_TIME, IC4_SPECIAL, CHECKER_DATE_TIME, CALLOVER_ID, POST_BRN, BATCH_NO, V_NUM, DOC_NO, DR_TXN_NGN, RATE, TXN_MNEM AS MNEM, AC_GL_BRN_NAME, 
                                    COD_BANK, TXN_MNEMONIC, TXN_BRANCH, AMOUNT, TXN_CODE,TIME_KEY, REF_NUM FROM CALLOVER_TRANSACTION_L3 A 
                                    WHERE  A.IC4_INPUTTER = %s 
                                    AND TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD') = %s
                                    AND A.CALLOVER_OFFICER IS NULL
                                    AND A.TXN_MNEMONIC = 'NORMAL'
                                    AND EXISTS ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 B
                                                    WHERE B.BRANCH_CODE = A.BRANCH_CODE 
                                                    AND TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')
                                                    AND B.TRANS_ID = A.TRANS_ID
                                                    AND ABS(B.LCY_AMOUNT) >= %s
                                                    AND B.CALLOVER_OFFICER IS NULL
                                                    AND B.TXN_MNEMONIC = 'NORMAL'
                                                ) 


                                    ) a ) a GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, 
                                    GRP_BY_USER, TXN_CODE
                                            
                                            ''',(id,request.session['transactionDate'],request.session['transLimit']))
    query_result =dictfetchall (initialcursor)
    print('singletransactionnnnnnnnnnnr',request.POST.get('singletran'))
    for index in range(len(query_result)):
    
        
        date_only = query_result[index]['GRP_BY_DATE'].strftime("%d-%m-%Y")
        callover_ID = str(query_result[index]['GRP_BY_USER']) + str(date_only) + query_result[index]['GRP_BY_REF']

        request.session['review'] =tomorrowf


        users = query_result[index]['GRP_BY_USER']
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
            my_id= str(query_result[index]['GRP_BY_USER'])+str(date_only) + query_result[index]['GRP_BY_REF']
        else:
            my_id= str(query_result[index]['GRP_BY_USER'])+ str(date_only) + query_result[index]['GRP_BY_REF']
        



    
            
    if(request.POST.get('singletran')):
        print('yes of single')
        transections = IC4_Callover_L3.objects.filter(Trans_ID=request.POST.get('singletran'))
        cursor=connection.cursor()
        for transection in transections:
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
                 ''',(today,todaye,str(query_result[index]['GRP_BY_USER'])+str(date_only) + request.POST.get('singletran'),request.session['username'],request.session['transactionDate'],request.POST.get('singletran'),request.session['selectedbranch'],query_result[index]['GRP_BY_USER']))
            # transection.Callover_ID = str(query_result[index]['GRP_BY_USER'])+str(date_only) + request.POST.get('singletran')
            # transection.Callover_Officer = username
            # transection.Callover_Date = today
            # transection.Callover_Time = todaye
            # transection.save()
            print ('single singletransid......................',request.POST.get('singletran'))
            accepted_transection = IC4_ACCEPTED_CALLOVER(CallOver_ID=id,
                                                                            GRP_BY_REF=request.POST.get('singletran'),
                                                                            GRP_BY_USER=query_result[index]['GRP_BY_USER'],
                                                                            GRP_BY_DATE=request.session['transactionDate'],
                                                                            Branch_Code=request.session['selectedbranch'],
                                                                            Callover_Officer=username,
                                                                            Tree_Key=5188,
                                                                            Ref_Num=voucher)
            accepted_transection.save()
    
    

            flag = True
            msg = ""
        
        
    else:
      
    


        if(status=="True"):
            msg = "stamp Not Found"
            Exp_id = 41

            transections = IC4_Callover_L3.objects.filter(IC4_Inputter=id, Entry_Date=request.session['transactionDate'])
            # json_trans=json.dumps(transections)
            # print("transectiooooooooooo",json_trans)
            for transection in transections:
                
                date_only = transection.Entry_Date.strftime("%d-%m-%Y")
                callover_ID = str(transection.IC4_Inputter) + str(date_only) + transection.Trans_ID

                request.session['review'] =tomorrowf


                users = str(transection.IC4_Inputter)
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
                    my_id= str(str(transection.IC4_Inputter))+str(date_only) + transection.Trans_ID
                else:
                    my_id= str(str(transection.IC4_Inputter))+ str(date_only) + transection.Trans_ID
                cursor=connection.cursor()
                if (abs(float(transection.LCY_Amount)) >= abs (float(request.session['transLimit']))):
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
                                ''',(today,todaye,id,username,request.session['transactionDate'],transection.Trans_ID,request.session['selectedbranch'],transection.IC4_Inputter))  
                    
                    
                    # transection.Callover_ID = id
                    # transection.Callover_Officer = username
                    # transection.Callover_Date = today
                    # transection.Callover_Time = todaye
                    # transection.save()
                    print ('transid......................',transection.Trans_ID)
                    accepted_transection = IC4_ACCEPTED_CALLOVER(CallOver_ID=id,
                                                                                    GRP_BY_REF=transection.Trans_ID,
                                                                                    GRP_BY_USER=transection.IC4_Inputter,
                                                                                    GRP_BY_DATE=transection.Entry_Date,
                                                                                    Branch_Code=transection.Branch_Code,
                                                                                    Callover_Officer=username,
                                                                                    Tree_Key=5188,
                                                                                    Ref_Num=voucher)
                    accepted_transection.save()
                    useractivity(request.session.session_key,"Callover for Control Special",socket.gethostbyname(socket.gethostname()),socket.gethostname(),
                    request.session['username'],
                    today_date,"""{0} called over transaction {1}""".format(username,str(transection.IC4_Inputter)),
                    "Callover for Control Special",request.session.session_key,"U-review","Callover",today,today_date)

            
        
                    flag = True
                    msg = ""
                else:
                    print("limit exceeded")

    flag = True
    msg = ""       
    exception_dict = ""
    if(flag==False):
        exception = IC4_Observation_Model.objects.get(pk=20)
        def obj_to_dict(obj):
            return obj.__dict__
        json_string = json.dumps(exception, default=obj_to_dict)
        exception_dict = json.loads(json_string)

    inputterEmail=''
    if (inputterEmail):
        print("yes")
        args = {
        
            'flag': flag,
            'msg': msg,
            'exception_result': exception_dict,
            'query_result': query_result[0],
            'today_date': todayc,
            'tomorrow': tomorrowf,
            'callover': username,
            'inputterEmail': 'u-review@unionbankng.com',
            'profileId': profileId, 
            'current_tim2': current_tim2
        }
    else:
        print("no")
        args = {
                'flag': flag,
                'msg': msg,
                'exception_result': exception_dict,
                'query_result': query_result,
                'today_date': todayc,
                'tomorrow': tomorrowf,
                'callover': username,
                'inputterEmail': 'u-review@unionbankng.com',
                'profileId': 'profileId', 
                'current_tim2': current_tim2
                }



    return JsonResponse(args)






def load(request):
    response = IC4_Callover_L3.objects.all().update(IP_Address='127.0.0.1:8090')
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