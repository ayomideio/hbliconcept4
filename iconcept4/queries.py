from datetime import datetime

# today_date = datetime.now()
# today_date = datetime.now().date()
today_date = "2018-JUL-19"
# today_date = datetime.strptime('2020-02-26 00:00:00.000000', "%Y-%m-%d %H:%M:%S.%f")


def get_query():
    # today_date = datetime.now()
    # today_date = today.strftime("%d-%b-%Y")
    # print(today_date)
    b_c = '000'
    today_date = '19-JUL-18'
    my_query=""" 
    SELECT IC4_BRANCH_CODE, GRP_BY_DATE, SUM(CALL_NO_OF_VOUCHERS) as NO_OF_ENTRIES, SUM(CALL_CREDIT_FREQ) as NO_OF_CREDIT, SUM(CALL_DEBIT_FREQ) as NO_OF_DEBIT, SUM(CALL_CREDIT_TOTAL) as CREDIT_TOTAL_CALL, SUM(CALL_DEBIT_TOTAL) as DEBIT_TOTAL_CALL 
FROM ( 

SELECT a.*, coalesce(p.USER_NAME,a.GRP_BY_USER) PROFILE_NAME FROM ( SELECT IC4_BRANCH_CODE, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, 
 SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, SUM(CREDIT) CALL_CREDIT_TOTAL, 
 SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, SUM(ABS(DEBIT)) as CALL_DEBIT_TOTAL, 
 SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE 
 FROM ( 	SELECT "TRANS_ID" GRP_BY_REF,
"BRANCH_CODE" IC4_BRANCH_CODE,
"ENTRY_DATE" GRP_BY_DATE, 
"IC4_INPUTTER" GRP_BY_USER, 
 CALLOVER_OFFICER, 
 		case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ,
 		case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ,
 		case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT,
 		case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT
 		from (

SELECT 
ID, 
trans_id,
TRANS_REF_ID,                                                    
TRANS_REF_ID AS REF_ID,                                                      
TRANS_SUB_ID AS AC_ENTRY_SR_NO,                                                                                                                                    
BRANCH_CODE,                                                                                             
BRANCH_NAME,
ACCOUNT_ID AS ACCOUNT_NUMBER,                                                        
ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME ,                                                                                          
LCY_CODE,   
FCY_AMOUNT,             
FCY_CODE,             
TRANS_CODE  AS TXN_C,                                    
TRANS_MODE as TRN_REF_NO,                                    
CHEQUE_NO,                           
NARRATIVE AS TRANSACTION_NARRATIVE,                                                                                                                                                                                                
ENTRY_DATE AS VALUE_DATE,       
TRAN_DATE,
BOOKING_DATE,              
POSTING_DATE,              
ENTRY_DATE,                
ENTRY_TIME,                
IC4_ACCOUNT_OFFICER,                 
IC4_INPUTTER ,                        
IC4_AUTHORISER ,                      
IC4_VERIFIER  ,
CHECKER_ID, 
MAKER_ID,                       
TEXT_FIELD_1  ,                                                      
TEXT_FIELD_2, 
AMT_FIELD_1,                                                     
to_char(AMT_FIELD_1, 'FM99,999,999,999,999.00')LCY_AMOUNT,           
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
TXN_MNEMONIC,                                                      
TXN_BRANCH,                                                        
AMOUNT,                 
TIME_KEY,
REF_NUM      

FROM CALLOVER_TRANSACTION
WHERE ENTRY_DATE = '19-JUL-18'
AND BRANCH_CODE <> '000'
AND TXN_MNEMONIC = 'NORMAL'
AND CALLOVER_OFFICER IS NULL
AND  ACCOUNT_NAME not like 'TILL-INTER%'
) a  ) a 
  GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER) a, PROFILE p WHERE a.GRP_BY_USER = p.PROFILE_ID(+) 
  ) GROUP BY GRP_BY_DATE, IC4_BRANCH_CODE
  ORDER BY GRP_BY_DATE, IC4_BRANCH_CODE

         """.format(today_date,b_c)

    return my_query

def trans_query(branch_id):

    my_query = """
    SELECT IC4_BRANCH_CODE, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, SUM(CREDIT) CALL_CREDIT_TOTAL, SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, SUM(ABS(DEBIT)) as CALL_DEBIT_TOTAL, SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE FROM ( SELECT "TRANS_ID" GRP_BY_REF, "BRANCH_CODE" IC4_BRANCH_CODE, "ENTRY_DATE" GRP_BY_DATE, "IC4_INPUTTER" GRP_BY_USER, CALLOVER_OFFICER, case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ, case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ, case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT, case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT from ( SELECT ID, trans_id, TRANS_REF_ID, TRANS_REF_ID AS REF_ID, TRANS_SUB_ID AS AC_ENTRY_SR_NO, BRANCH_CODE, BRANCH_NAME, ACCOUNT_ID AS ACCOUNT_NUMBER, ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME , LCY_CODE, FCY_AMOUNT, FCY_CODE, TRANS_CODE  AS TXN_C, TRANS_MODE as TRN_REF_NO, CHEQUE_NO, NARRATIVE AS TRANSACTION_NARRATIVE, ENTRY_DATE AS VALUE_DATE, TRAN_DATE, BOOKING_DATE, POSTING_DATE, ENTRY_DATE, ENTRY_TIME, IC4_ACCOUNT_OFFICER, IC4_INPUTTER , IC4_AUTHORISER , IC4_VERIFIER  , CHECKER_ID, MAKER_ID, TEXT_FIELD_1  , TEXT_FIELD_2, AMT_FIELD_1, AMT_FIELD_2, DATE_FIELD_1, DATE_FIELD_2 , CALLOVER_REMARK, EXCEPTION_ID, SEVERITY_ID, REVIEW_DATE, CALLOVER_OFFICER, CALLOVER_DATE, CALLOVER_TIME, IC4_SPECIAL, CHECKER_DATE_TIME, CALLOVER_ID, POST_BRN, BATCH_NO, V_NUM, DOC_NO, DR_TXN_NGN, RATE, TXN_MNEM AS MNEM, AC_GL_BRN_NAME, COD_BANK, TXN_MNEMONIC, TXN_BRANCH, AMOUNT, TIME_KEY, REF_NUM FROM callover_transaction WHERE TXN_MNEMONIC = 'NORMAL' AND CALLOVER_OFFICER IS NULL AND  ACCOUNT_NAME not like 'TILL-INTER%' ) a ) a  GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER
   
     """
    return my_query

def trans_query_profiles(profile_id):

    my_query = """SELECT IC4_BRANCH_CODE, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, SUM(CREDIT) CALL_CREDIT_TOTAL, SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, SUM(ABS(DEBIT)) as CALL_DEBIT_TOTAL, SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE FROM ( SELECT "TRANS_ID" GRP_BY_REF, "BRANCH_CODE" IC4_BRANCH_CODE, "ENTRY_DATE" GRP_BY_DATE, "IC4_INPUTTER" GRP_BY_USER, CALLOVER_OFFICER, case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ, case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ, case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT, case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT from ( SELECT ID, trans_id, TRANS_REF_ID, TRANS_REF_ID AS REF_ID, TRANS_SUB_ID AS AC_ENTRY_SR_NO, BRANCH_CODE, BRANCH_NAME, ACCOUNT_ID AS ACCOUNT_NUMBER, ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME , LCY_CODE, FCY_AMOUNT, FCY_CODE, TRANS_CODE  AS TXN_C, TRANS_MODE as TRN_REF_NO, CHEQUE_NO, NARRATIVE AS TRANSACTION_NARRATIVE, ENTRY_DATE AS VALUE_DATE, TRAN_DATE, BOOKING_DATE, POSTING_DATE, ENTRY_DATE, ENTRY_TIME, IC4_ACCOUNT_OFFICER, IC4_INPUTTER , IC4_AUTHORISER , IC4_VERIFIER  , CHECKER_ID, MAKER_ID, TEXT_FIELD_1  , TEXT_FIELD_2, AMT_FIELD_1, AMT_FIELD_2, DATE_FIELD_1, DATE_FIELD_2 , CALLOVER_REMARK, EXCEPTION_ID, SEVERITY_ID, REVIEW_DATE, CALLOVER_OFFICER, CALLOVER_DATE, CALLOVER_TIME, IC4_SPECIAL, CHECKER_DATE_TIME, CALLOVER_ID, POST_BRN, BATCH_NO, V_NUM, DOC_NO, DR_TXN_NGN, RATE, TXN_MNEM AS MNEM, AC_GL_BRN_NAME, COD_BANK, TXN_MNEMONIC, TXN_BRANCH, AMOUNT, TIME_KEY, REF_NUM FROM callover_transaction WHERE ENTRY_DATE = '{1}' AND BRANCH_CODE <> '000' AND IC4_INPUTTER='{0}' AND TXN_MNEMONIC = 'NORMAL' AND CALLOVER_OFFICER IS NULL AND  ACCOUNT_NAME not like 'TILL-INTER%' ) a ) a  GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER """.format(profile_id,today_date)
    
    return my_query

def acc_query(trans_id):
    branch = '000'
    q = """SELECT ID, Trans_ID, TRANS_REF_ID,
     TRANS_REF_ID AS REF_ID, TRANS_SUB_ID AS AC_ENTRY_SR_NO, BRANCH_CODE, BRANCH_NAME, ACCOUNT_ID AS ACCOUNT_NUMBER, 
     ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME , LCY_CODE,LCY_AMOUNT, FCY_AMOUNT, FCY_CODE, TRANS_CODE  AS TXN_C, TRANS_MODE as 
     TRN_REF_NO, CHEQUE_NO, NARRATIVE AS TRANSACTION_NARRATIVE, ENTRY_DATE AS VALUE_DATE, TRAN_DATE, BOOKING_DATE, POSTING_DATE,
      ENTRY_DATE, ENTRY_TIME, IC4_ACCOUNT_OFFICER, IC4_INPUTTER , IC4_AUTHORISER , IC4_VERIFIER, CHECKER_ID, MAKER_ID, TEXT_FIELD_1 
       , TEXT_FIELD_2, AMT_FIELD_1, AMT_FIELD_2, DATE_FIELD_1, DATE_FIELD_2 , CALLOVER_REMARK, EXCEPTION_ID, SEVERITY_ID, REVIEW_DATE, 
       CALLOVER_OFFICER, CALLOVER_DATE, CALLOVER_TIME, IC4_SPECIAL, CHECKER_DATE_TIME, CALLOVER_ID, POST_BRN, BATCH_NO, V_NUM, 
       DOC_NO, DR_TXN_NGN, RATE, TXN_MNEM AS MNEM, AC_GL_BRN_NAME, COD_BANK, TXN_MNEMONIC, TXN_BRANCH, AMOUNT, TIME_KEY, 
       REF_NUM FROM callover_transaction WHERE  ENTRY_DATE = '{2}' AND BRANCH_CODE <> '{0}' 
       AND TXN_MNEMONIC = 'NORMAL' AND CALLOVER_OFFICER IS NULL AND  
       ACCOUNT_NAME not like 'TILL-INTER%' AND Trans_ID = '{1}'""".format(branch,trans_id,today_date)
    
    return q

def custom_query(trans_Id):

    my_query = """SELECT IC4_BRANCH_CODE, GRP_BY_REF,GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, TXN_CODE, SUM(CREDIT_FREQ + DEBIT_FREQ) as CALL_NO_OF_VOUCHERS, SUM(CREDIT_FREQ) CALL_CREDIT_FREQ, SUM(CREDIT) CALL_CREDIT_TOTAL, SUM(DEBIT_FREQ) CALL_DEBIT_FREQ, SUM(ABS(DEBIT)) as CALL_DEBIT_TOTAL, SUM(CREDIT - ABS(DEBIT)) as CALL_DIFFERENCE FROM ( SELECT "TRANS_ID" GRP_BY_REF, "TXN_CODE" TXN_CODE, "BRANCH_CODE" IC4_BRANCH_CODE, "ENTRY_DATE" GRP_BY_DATE, "IC4_INPUTTER" GRP_BY_USER, CALLOVER_OFFICER, case when "AMT_FIELD_1" >=0 then 1 else 0 end as CREDIT_FREQ, case when "AMT_FIELD_1" <0 then 1 else 0 end as DEBIT_FREQ, case when "AMT_FIELD_1" >=0 then "AMT_FIELD_1" else 0 end as CREDIT, case when "AMT_FIELD_1" <0 then "AMT_FIELD_1" else 0 end as DEBIT from ( SELECT ID, trans_id, TRANS_REF_ID, TRANS_REF_ID AS REF_ID, TRANS_SUB_ID AS AC_ENTRY_SR_NO, BRANCH_CODE, BRANCH_NAME, ACCOUNT_ID AS ACCOUNT_NUMBER, ACCOUNT_NAME AS CUSTOMER_ACCOUNT_NAME , LCY_CODE, FCY_AMOUNT, FCY_CODE, TRANS_CODE  AS TXN_C, TRANS_MODE as TRN_REF_NO, CHEQUE_NO, NARRATIVE AS TRANSACTION_NARRATIVE, ENTRY_DATE AS VALUE_DATE, TRAN_DATE, BOOKING_DATE, POSTING_DATE, ENTRY_DATE, ENTRY_TIME, IC4_ACCOUNT_OFFICER, IC4_INPUTTER , IC4_AUTHORISER , IC4_VERIFIER  , CHECKER_ID, MAKER_ID, TEXT_FIELD_1  , TEXT_FIELD_2, AMT_FIELD_1, AMT_FIELD_2, DATE_FIELD_1, DATE_FIELD_2 , CALLOVER_REMARK, EXCEPTION_ID, SEVERITY_ID, REVIEW_DATE, CALLOVER_OFFICER, CALLOVER_DATE, CALLOVER_TIME, IC4_SPECIAL, CHECKER_DATE_TIME, CALLOVER_ID, POST_BRN, BATCH_NO, V_NUM, DOC_NO, DR_TXN_NGN, RATE, TXN_MNEM AS MNEM, AC_GL_BRN_NAME, COD_BANK, TXN_MNEMONIC, TXN_BRANCH, AMOUNT, TXN_CODE,TIME_KEY, REF_NUM FROM callover_transaction WHERE  BRANCH_CODE <> '000' AND trans_id = '{0}' AND TXN_MNEMONIC = 'NORMAL' AND ACCOUNT_NAME not like 'TILL-INTER%' ) a ) a GROUP BY IC4_BRANCH_CODE, GRP_BY_REF, GRP_BY_DATE, CALLOVER_OFFICER, GRP_BY_USER, TXN_CODE""".format(trans_Id)
    
    return my_query
    
def ob_query(Selected):

    puery = """SELECT SEVERITY_LEVEL,IMPLICATION,ACTION FROM observation_model WHERE DESCRIPTION ='{0}'""".format(Selected)
    
    return puery

def comfig_query():

    huery = """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME ='CalloverExceptionAlertMessage'"""
    return huery
    

def ldap_query():

    lhuery = """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME='LdapAuthentication' """
    
    return lhuery
def ldap_url():

    urlhuery = """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME='LdapConnectionUrl' """
    
    return urlhuery
def ldap_domain():

    dohuery = """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME='LdapAuthenticationDomain' """
    
    return dohuery

def ldap_dn():

    dnhuery = """SELECT CONF_VALUE FROM IC4_CORE_CONFIGURATIONS WHERE NAME='LdapUserDn' """
    
    return dnhuery

def usergrp_query(username):

    grppuery = """SELECT GROUP_NAME FROM USERROLE WHERE USER_ID ='{0}'""".format(username)
    
    return grppuery
