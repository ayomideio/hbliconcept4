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

# #DataFlair
# def index(request):
#     shelf = Book.objects.all()
#     return render(request, 'book/library.html', {'shelf': shelf})
# def testing(request):
#     shelf=Book.objects.all()
#     return render(request,'book/abc.html',{'shelf':shelf})
# def upload(request):
#     upload = BookCreate()
#     if request.method == 'POST':
#         upload = BookCreate(request.POST, request.FILES)
#         if upload.is_valid():
#             upload.save()
#             return redirect('index')
#         else:
#             return HttpResponse("""your form is wrong, reload on <a href = "{{ url : 'index'}}">reload</a>""")
#     else:
#         return render(request, 'book/upload_form.html', {'upload_form':upload})
# def update_book(request, book_id):
#     book_id = int(book_id)
#     try:
#         book_sel = Book.objects.get(id = book_id)
#     except Book.DoesNotExist:
#         return redirect('index')
#     book_form = BookCreate(request.POST or None, instance = book_sel)
#     if book_form.is_valid():
#        book_form.save()
#        return redirect('index')
#     return render(request, 'book/upload_form.html', {'upload_form':book_form})
# def delete_book(request, book_id):
#     book_id = int(book_id)
#     try:
#         book_sel = Book.objects.get(id = book_id)
#     except Book.DoesNotExist:
#         return redirect('index')
#     book_sel.delete()
#     return redirect('index')
# @staff_member_required
# def index(request):
#
#     pagen=9
#     # pagen = request.POST['page']
#     shelf = Employee.objects.all()
#     paginator=Paginator(shelf,pagen)
#
#     page= request.GET.get('page')
#     shelf=paginator.get_page(page)
#     return render(request, 'book/library.html', {'shelf': shelf})
branch_cd="0"
def indexoflogin(request):
    if(request.POST.get('username')):
        username=request.POST.get('username')
        password=request.POST.get('password')
        cursor = connection.cursor()
        query=""" SELECT * FROM IC4_PRO_USERS  where USER_ID='{0}' and USER_PWD='{1}'  """.format(username,password)
        cursor.execute(query)
        yList = dictfetchall(cursor)
    
        if yList:
            # print(yList)

            global branch_cd
            branch_cd="010"
            # branch=yList.BRANCH_CODE
            print(yList)
            request.session['userparam'] = request.POST.get('username')
            query3 = '''SELECT BRANCH_CODE FROM IC4_PRO_USERS WHERE USER_ID='{0}'  '''.format(username)
            cursor3=connection.cursor()
            cursor3.execute(query3)
            yList3 = dictfetchall(cursor3)
            branch=''
            for index in range(len(yList3)):
                for key in yList3[index]:
                    branch=yList3[index][key]
                    print(branch)
            request.session['secondarybranch'] =branch
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'allauth/account/login.html', {"error": "username or password incorrect"})
    return render(request, 'allauth/account/login.html', {"": ""})
def index(request):
    b_c = ''
    transLimit=request.POST.get('transLimit')
    request.session['transLimit']=0
    
    if (transLimit is not  None):
      
        request.session['transLimit']=transLimit

    if('transLimit' in request.session):
       
        # request.session['transLimit']=transLimit
        username=request.session['username']
        pbranch=request.session['secondarybranch']
        today_date = '19-JUL-18'
        query2 = '''SELECT BRANCH_CODE FROM USER_BRANCHES WHERE USER_ID='{0}'  '''.format(username)
        cursor2=connection.cursor()
        result2=cursor2.execute(query2)
        yList2=dictfetchall(cursor2)
        # print(yList2)
        for index in range(len(yList2)):
            for key in yList2[index]:
                b_c+=yList2[index][key]+","
            
                # print(yList2[index][key])
                # print(b_c)
        b_c+=request.session['secondarybranch']
        x = b_c.split(',')

        b_c=str(x)[1:-1]
        print(b_c)

        cursor = connection.cursor()
        result = cursor.execute('''
                SELECT IC4_BRANCH_CODE, GRP_BY_DATE, SUM(CALL_NO_OF_VOUCHERS) as NO_OF_ENTRIES, SUM(CALL_CREDIT_FREQ) as NO_OF_CREDIT, SUM(CALL_DEBIT_FREQ) as NO_OF_DEBIT, SUM(CALL_CREDIT_TOTAL) as CREDIT_TOTAL_CALL, SUM(CALL_DEBIT_TOTAL) as DEBIT_TOTAL_CALL 
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
                        (CASE when substr(trans_id,1,1) ='M' then '0'||lpad(substr(trans_id,2,length(trans_id)),6,'0')when substr(trans_id,1,1) ='S' then '00'|| substr(trans_id,2,length(trans_id)) else trans_id end ) AS TRANS_ID,
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
                       
                       
                        AND A.CALLOVER_OFFICER IS NULL
                            AND EXISTS ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 B
             WHERE  B.BRANCH_CODE = A.BRANCH_CODE 
             AND TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')
             AND B.TRANS_ID = A.TRANS_ID
             AND ABS(B.AMT_FIELD_1) >= {1}
             AND B.CALLOVER_OFFICER IS NULL 
          )
                        ) a  ) a 
                        GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                        ) GROUP BY GRP_BY_DATE, IC4_BRANCH_CODE
                        ORDER BY GRP_BY_DATE, IC4_BRANCH_CODE

        '''.format(b_c,request.session['transLimit']), None)

        yList = dictfetchall(cursor)
    
        columns = [col[0] for col in cursor.description]
        # print(yList)
        # profiles = IC4_Profile.objects.all()

        profiles = Profile.objects.all()
    
        return render(request, 'calloverforcontrol_book/library.html', {'results':yList, 'Profiles':profiles, 'test':branch_cd,'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})


   

    
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
def Bank_Trans(request, branch_id):
    transactionDate=request.POST.get('dateVal')
    request.session['transactionDate']=transactionDate
    print(transactionDate,"transactionDaste")
    request.session['arraytest']=""
    query = trans_query(branch_id)
    cursor = connection.cursor()
    result = cursor.execute("""
                    SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
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
                (CASE when substr(trans_id,1,1) ='M' then '0'||lpad(substr(trans_id,2,length(trans_id)),6,'0')when substr(trans_id,1,1) ='S' then '00'|| substr(trans_id,2,length(trans_id)) else trans_id end ) AS TRANS_ID,
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
                WHERE  A.BRANCH_CODE = '{0}'
                AND TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD') = '{1}'
                AND A.CALLOVER_OFFICER IS NULL

                        AND EXISTS ( SELECT DISTINCT B.TRANS_ID FROM U_IC4INDEP.CALLOVER_TRANSACTION_L3 B
                            WHERE  B.BRANCH_CODE = A.BRANCH_CODE 
                            AND TO_CHAR(B.ENTRY_DATE, 'YYYY-MM-DD') = TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD')
                            AND B.TRANS_ID = A.TRANS_ID
                            AND ABS(B.AMT_FIELD_1) >= {2}
                    )
                ) a  ) a 
                GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                            
                """.format(branch_id,request.session['transactionDate'],request.session['transLimit']), None)
    request.session['selectedbranch'] =branch_id
    
    yList = dictfetchall(cursor)
    request.session['arraytest']=""
    # request.session['arraytest']=[{'IC4_BRANCH_CODE': '010', 'GRP_BY_REF': '010CHDP182000006', 'CALLOVER_OFFICER': None, 'GRP_BY_USER': 'CHIAMAECHI', 'CALL_NO_OF_VOUCHERS': 2, 'CALL_CREDIT_FREQ': 1, 'CALL_CREDIT_TOTAL': 2300, 'CALL_DEBIT_FREQ': 1, 'CALL_DEBIT_TOTAL': 2300, 'CALL_DIFFERENCE': 0}, {'IC4_BRANCH_CODE': '010', 'GRP_BY_REF': '010CHDP182000515',  'CALLOVER_OFFICER': None, 'GRP_BY_USER': 'FCAGU', 'CALL_NO_OF_VOUCHERS': 2, 'CALL_CREDIT_FREQ': 1, 'CALL_CREDIT_TOTAL': 4000, 'CALL_DEBIT_FREQ': 1, 'CALL_DEBIT_TOTAL': 4000, 'CALL_DIFFERENCE': 0}]
    # print(yList)

    return render(request, 'calloverforcontrol/branch_trans.html', {'results': yList,'username':request.session['userparam'],'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})

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
        SELECT USER_ID, FIRST_NAME FROM IC4_PRO_USERS lst WHERE BRANCH_CODE = '{0}' AND USER_ROLE IN('BSM', 'HEADTELLER')
        """.format(request.session['selectedbranch']),None)
        yLists = dictfetchall(resultss)

        yList=None
        cursor2 = connection.cursor()
        cursor2.execute(""" SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
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
                    (CASE when substr(trans_id,1,1) ='M' then '0'||lpad(substr(trans_id,2,length(trans_id)),6,'0')when substr(trans_id,1,1) ='S' then '00'|| substr(trans_id,2,length(trans_id)) else trans_id end ) AS TRANS_ID,
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
                    WHERE  A.BRANCH_CODE = '{0}'
                    AND TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD') = '{1}'
                    AND A.CALLOVER_OFFICER IS NULL
                        
                    ) a  ) a 
                    GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                        
     """.format(request.session['selectedbranch'],request.session['transactionDate']), None)
        list=cursor2.fetchall()
        list2 = random.choice(list)						
        print(list2)
        if (list2):
            cursor13 = connection.cursor()
            cursor13.execute("""
                            SELECT 
                        ID,
                        (CASE when substr(trans_id,1,1) ='M' then '0'||lpad(substr(trans_id,2,length(trans_id)),6,'0') when substr(trans_id,1,1) ='S' then '00'|| substr(trans_id,2,length(trans_id)) else trans_id end ) AS TRANS_ID,
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
                        WHERE  A.BRANCH_CODE = '{1}'
                        AND (CASE when substr(A.trans_id,1,1) ='M' then '0'||lpad(substr(A.trans_id,2,length(A.trans_id)),6,'0') 
                                            when substr(A.trans_id,1,1) ='S' then '00'|| substr(A.trans_id,2,length(A.trans_id)) 
                                            else A.trans_id end ) ='{0}'
                        AND TRUNC(A.ENTRY_DATE)='{2}'
                        AND A.CALLOVER_OFFICER IS NULL
                        """.format(list2[1],request.session['selectedbranch'],list2[2]),None)
            
            cursor14=connection.cursor()
            cursor14.execute("""
                            SELECT 
                        ID,
                        (CASE when substr(trans_id,1,1) ='M' then '0'||lpad(substr(trans_id,2,length(trans_id)),6,'0') when substr(trans_id,1,1) ='S' then '00'|| substr(trans_id,2,length(trans_id)) else trans_id end ) AS TRANS_ID,
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
                        WHERE  A.BRANCH_CODE = '{1}'
                        AND (CASE when substr(A.trans_id,1,1) ='M' then '0'||lpad(substr(A.trans_id,2,length(A.trans_id)),6,'0') 
                                            when substr(A.trans_id,1,1) ='S' then '00'|| substr(A.trans_id,2,length(A.trans_id)) 
                                            else A.trans_id end ) ='{0}'
                        AND TRUNC(A.ENTRY_DATE)='{2}'
                        AND A.CALLOVER_OFFICER IS NULL
                        """.format(list2[1],request.session['selectedbranch'],list2[2]),None)
            

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
            return render(request, 'calloverforcontrol/acc_trans.html', {'calloverurl':request.session['calloverurl'],'nexttran':nxt,'tran':request.session['selectedbranch'],'cb':request.session['arraytest'],'results': yList2,'username':request.session['userparam'], 'trans_ID':lst3[2],'yListr':yListr,'yLists':yLists,'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
        else:
            return HttpResponseRedirect(reverse('calloverforcontrol_index'))


    else:
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
        SELECT USER_ID, FIRST_NAME FROM IC4_PRO_USERS lst WHERE BRANCH_CODE = '{0}' AND USER_ROLE IN('BSM', 'HEADTELLER')
        """.format(request.session['selectedbranch']),None)
        yLists = dictfetchall(resultss)


        query = acc_query(trans_id)
        cursor = connection.cursor()
        results = cursor.execute("""

        
                        
                    SELECT 
                        ID,
                        (CASE when substr(trans_id,1,1) ='M' then '0'||lpad(substr(trans_id,2,length(trans_id)),6,'0') when substr(trans_id,1,1) ='S' then '00'|| substr(trans_id,2,length(trans_id)) else trans_id end ) AS TRANS_ID,
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
                        WHERE  A.BRANCH_CODE = '{1}'
                        AND (CASE when substr(A.trans_id,1,1) ='M' then '0'||lpad(substr(A.trans_id,2,length(A.trans_id)),6,'0') 
                                            when substr(A.trans_id,1,1) ='S' then '00'|| substr(A.trans_id,2,length(A.trans_id)) 
                                            else A.trans_id end ) ='{0}'
                        AND TRUNC(A.ENTRY_DATE)='{2}'
                        AND A.CALLOVER_OFFICER IS NULL

                    """.format(trans_id,request.session['selectedbranch'] ,request.session['entry_date']),None)
        print('>>>>>>>>>>>>',trans_id)
        print('>>>>>>>>>>>>',request.session['selectedbranch'])
        print('>>>>>>>>>>>>',tst)
        cursor2=connection.cursor()
        secondtrans_id=cursor2.execute("""

        
                        
                    SELECT 
                        ID,
                        (CASE when substr(trans_id,1,1) ='M' then '0'||lpad(substr(trans_id,2,length(trans_id)),6,'0') when substr(trans_id,1,1) ='S' then '00'|| substr(trans_id,2,length(trans_id)) else trans_id end ) AS TRANS_ID,
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
                        WHERE  A.BRANCH_CODE = '{1}'

                        AND (CASE when substr(A.trans_id,1,1) ='M' then '0'||lpad(substr(A.trans_id,2,length(A.trans_id)),6,'0') 
                                            when substr(A.trans_id,1,1) ='S' then '00'|| substr(A.trans_id,2,length(A.trans_id)) 
                                            else A.trans_id end ) ='{0}'
                        AND TRUNC(A.ENTRY_DATE)='{2}'
                        AND A.CALLOVER_OFFICER IS NULL

                """.format(trans_id,request.session['selectedbranch'] ,request.session['entry_date']),None)
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
            return render(request, 'calloverforcontrol/acc_trans.html', {'calloverurl':request.session['calloverurl'],'tran':request.session['selectedbranch'],'cb':request.session['arraytest'],'results': yList,'username':request.session['userparam'],  'trans_ID':list2[2],'yListr':yListr,'yLists':yLists,'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
        else:
            yList=None
            cursor2 = connection.cursor()
            cursor2.execute(""" SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
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
                        (CASE when substr(trans_id,1,1) ='M' then '0'||lpad(substr(trans_id,2,length(trans_id)),6,'0')when substr(trans_id,1,1) ='S' then '00'|| substr(trans_id,2,length(trans_id)) else trans_id end ) AS TRANS_ID,
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
                        WHERE  A.BRANCH_CODE = '{0}'
                        AND TO_CHAR(A.ENTRY_DATE, 'YYYY-MM-DD') = '{1}'
                        AND A.CALLOVER_OFFICER IS NULL
                            
                        ) a  ) a 
                        GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, U_IC4INDEP.PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
                            
        """.format(request.session['selectedbranch'],request.session['transactionDate']), None)
            list2=cursor2.fetchone()
            if (list2):
                cursor13 = connection.cursor()
                cursor13.execute("""
                                SELECT 
                            ID,
                            (CASE when substr(trans_id,1,1) ='M' then '0'||lpad(substr(trans_id,2,length(trans_id)),6,'0') when substr(trans_id,1,1) ='S' then '00'|| substr(trans_id,2,length(trans_id)) else trans_id end ) AS TRANS_ID,
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
                            WHERE  A.BRANCH_CODE = '{1}'
                            AND (CASE when substr(A.trans_id,1,1) ='M' then '0'||lpad(substr(A.trans_id,2,length(A.trans_id)),6,'0') 
                                                when substr(A.trans_id,1,1) ='S' then '00'|| substr(A.trans_id,2,length(A.trans_id)) 
                                                else A.trans_id end ) ='{0}'
                            AND TRUNC(A.ENTRY_DATE)='{2}'
                            AND A.CALLOVER_OFFICER IS NULL
                            """.format(list2[1],request.session['selectedbranch'],list2[2]),None)
                
                cursor14=connection.cursor()
                cursor14.execute("""
                                SELECT 
                            ID,
                            (CASE when substr(trans_id,1,1) ='M' then '0'||lpad(substr(trans_id,2,length(trans_id)),6,'0') when substr(trans_id,1,1) ='S' then '00'|| substr(trans_id,2,length(trans_id)) else trans_id end ) AS TRANS_ID,
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
                            WHERE  A.BRANCH_CODE = '{1}'
                            AND (CASE when substr(A.trans_id,1,1) ='M' then '0'||lpad(substr(A.trans_id,2,length(A.trans_id)),6,'0') 
                                                when substr(A.trans_id,1,1) ='S' then '00'|| substr(A.trans_id,2,length(A.trans_id)) 
                                                else A.trans_id end ) ='{0}'
                            AND TRUNC(A.ENTRY_DATE)='{2}'
                            AND A.CALLOVER_OFFICER IS NULL
                            """.format(list2[1],request.session['selectedbranch'],list2[2]),None)
                

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
                return render(request, 'calloverforcontrol/acc_trans.html', {'calloverurl':request.session['calloverurl'],'nexttran':nxt,'tran':request.session['selectedbranch'],'cb':request.session['arraytest'],'results': yList2,'username':request.session['userparam'], 'trans_ID':lst3[2],'yListr':yListr,'yLists':yLists,'grouplist':request.session['grouplist'],'grouplistbsm':request.session['grouplistbsm'],'grouplistbc':request.session['grouplistbc'],'grouplisttrs':request.session['grouplisttrs'],'grouplisttrc':request.session['grouplisttrc'],'grouplistcon':request.session['grouplistcon'],'grouplistfot':request.session['grouplistfot'],'grouplistfoc':request.session['grouplistfoc'],'grouplist_ce':request.session['grouplist_ce'],'grouplist_ca':request.session['grouplist_ca'],'grouplist_db':request.session['grouplist_db'],'grouplist_ei':request.session['grouplist_ei']})
            else:
                return HttpResponseRedirect(reverse('calloverforcontrol_index'))







import json
from datetime import timedelta
from datetime import date
import numpy as np
@csrf_exempt
def Observation(request):
    print("Getting other details from observation model......")
   
    Selected = request.POST['selected']
    request.session['selected'] = Selected
    query_result = __get_ob_result(Selected) 
    severity = query_result['severity']
    implication = query_result['implication']
    action = query_result['action']
    request.session['severity'] = severity
    request.session['implication'] = implication
    request.session['action'] = action
    # callover_ID = str(query_result['user']) + str(date_only) + query_result['trans_id']
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
    calloverDate = request.POST['calloverDate']
    reviewDate = request.POST['reviewDate']
    officer = request.POST['officer']
    observation=request.session['selected'] 
    exceptionDetails = request.POST['exceptionDetails']
    implication = request.POST['implication']
    Severity = request.POST['severity']
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
    Ownerdetails ='Pending Callover for Tellers'


    Supervisor =bsmheadteller
    reviewDate=datetime.strptime(reviewDate, '%d-%m-%Y')
    print(reviewDate)
    calloverDate=datetime.strptime(calloverDate, '%d-%m-%Y')
    print(calloverDate)
    enteryDate=datetime.strptime(enteryDate, '%d-%m-%Y')
    print(enteryDate)

    

    exception_transection = IC4_CALLOVER_EXCEPTION(CallOver_ID=calloverID, Owner_Detail=officer,Callover_Level=Calloverlevel, Branch_Code= branchCode, Maturity_Rating=transID, Inputter_Email=inputterEmail, Callover_Officer=officer, Severity_Level=Severity, Implication=implication, Action=action, Exception_Detail=exceptionDetails, Observation=observation, Issue_Priority=enteryDate, Callover_Date=calloverDate, Review=reviewDate,Supervisor=bsmheadteller,Tree_ID=5188,Exception_Status='OPEN')

    exception_transection.save()
    __update_callover2(transID, calloverID, Severity,reviewDate)
    flag = True
    msg = "Exception Save Successfully"

    query_result = __get_config_result()
    html_content = query_result['html_text']
    # print(html_content)
    html_content2=str(html_content)
    # print(html_content2)

    html_content2=html_content2.replace("$ExceptionTemplate.$Reference", transID)
    html_content2=html_content2.replace("$ExceptionTemplate.$Datee",str(enteryDate2))
    html_content2=html_content2.replace("$ExceptionTemplate.$Severity", Severity)
    html_content2=html_content2.replace("$ExceptionTemplate.$Message", exceptionDetails)
    html_content2=html_content2.replace("$ExceptionTemplate.$Implication",implication)
    html_content2=html_content2.replace("$ExceptionTemplate.$Action", action)

    html_content2=html_content2.replace("$ExceptionTemplate.$Inputter",inputterEmail)
    html_content2=html_content2.replace("$ExceptionTemplate.$Bcode", branchCode)
        

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
def delete_book(request, id):
    id = int(id)
    try:
        IC4_trans_obj = IC4_Callover_L3.objects.get(id = id)
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

def __get_query_result(trasn_id):
    print('>>>>>>>>>>>>>>>>>>',trasn_id)
    query = '''SELECT IC4_BRANCH_CODE, TRANS_ID_1, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, TXN_CODE, 
SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, 
SUM(CREDIT) CALL_CREDIT_TOTAL, SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, SUM(ABS(DEBIT)) as CALL_DEBIT_TOTAL, 
SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE FROM ( SELECT "TRANS_ID_1" TRANS_ID_1, "TRANS_ID" GRP_BY_REF, 
"TXN_CODE" TXN_CODE, "BRANCH_CODE" IC4_BRANCH_CODE, "ENTRY_DATE" GRP_BY_DATE, 
"IC4_INPUTTER" GRP_BY_USER, CALLOVER_OFFICER, 
case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ, case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ, 
case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT, case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT 
from ( 
SELECT ID, 
(CASE when substr(trans_id,1,1) ='M' then '0'||lpad(substr(trans_id,2,length(trans_id)),6,'0') 
                    when substr(trans_id,1,1) ='S' then '00'|| substr(trans_id,2,length(trans_id)) 
                    else trans_id end ) AS TRANS_ID, TRANS_ID AS TRANS_ID_1,
TRANS_REF_ID, TRANS_REF_ID AS REF_ID, TRANS_SUB_ID AS TXN_SUB_ID, 
BRANCH_CODE, BRANCH_NAME, ACCOUNT_ID AS ACCOUNT_NUMBER, ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME , 
LCY_CODE, FCY_AMOUNT, FCY_CODE, TRANS_CODE  AS TXN_C, TRANS_ID as TRN_REF_NO, CHEQUE_NO, 
NARRATIVE AS TRANSACTION_PARTICULAR, ENTRY_DATE AS VALUE_DATE, TRAN_DATE, BOOKING_DATE, 
POSTING_DATE, ENTRY_DATE, ENTRY_TIME, IC4_ACCOUNT_OFFICER, IC4_INPUTTER , IC4_AUTHORISER , 
IC4_VERIFIER  , CHECKER_ID, MAKER_ID, TEXT_FIELD_1  , TEXT_FIELD_2, AMT_FIELD_1, AMT_FIELD_2, 
DATE_FIELD_1, DATE_FIELD_2 , CALLOVER_REMARK, EXCEPTION_ID, SEVERITY_ID, REVIEW_DATE, 
CALLOVER_OFFICER, CALLOVER_DATE, CALLOVER_TIME, IC4_SPECIAL, CHECKER_DATE_TIME, CALLOVER_ID, 
POST_BRN, BATCH_NO, V_NUM, DOC_NO, DR_TXN_NGN, RATE, TXN_MNEM AS MNEM, AC_GL_BRN_NAME, COD_BANK, 
TXN_MNEMONIC, TXN_BRANCH, AMOUNT, TXN_CODE,TIME_KEY AS TENOR, REF_NUM 
FROM CALLOVER_TRANSACTION_L3 
WHERE  TRANS_ID = '{0}' 


) a ) a GROUP BY IC4_BRANCH_CODE, TRANS_ID_1, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, TXN_CODE'''.format(trasn_id)
    cursor = connection.cursor()
    results = cursor.execute(query)
    
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

def __update_callover(trans_id,callover_id,date, time, username):
   
    transections = IC4_Callover_L3.objects.filter(Trans_ID=trans_id)
    for transection in transections:
        transection.Callover_ID = callover_id
        transection.Callover_Officer = username
        transection.Callover_Date = date
        transection.Callover_Time = time
        transection.save()

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
        branchCode=query_result['branch']
            initialdate=query_result['date']
            grpbuuser=query_result['user']
            __update_callover(id,  my_id, today, todaye,username,branchCode,initialdate,grpbuuser)
            

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

    exception_transection = IC4_CALLOVER_EXCEPTION(CallOver_ID=callover_ID, Branch_Code= branchCode, Trans_ID=transID, IC4_Inputter=inputterEmail, Callover_Officer=officer, Severity_Level=severity, Implication=implication, Action=action, Exception_Details=exceptionDetails, Observation=observation, Entery_Date=enteryDate, Callover_Date=calloverDate, Review=reviewDate,Exception_Status='OPEN')

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