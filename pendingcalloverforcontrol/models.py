from django.db import models
from django.utils import timezone

LCY_Codes = (
    ('USD', 'USD'),
    ('NGN', 'NGN'),
)
Trans_Choices = (
    ('Credit', 'CREDIT'),
    ('Debit', 'DEBIT'),
)
Trans_Codes = (
    ('Credit','C'),
    ('Debit','D')
)
# Create your models here.
class IC4_Callover(models.Model):
    class Meta:
        db_table='CALLOVER_WAITING_L3'
    Trans_ID =  models.CharField(max_length=255, default="abc")
    Trans_Ref_ID =  models.CharField(max_length=65)
    Trans_Sub_ID =  models.CharField(max_length=245)
    Branch_Code = models.CharField(max_length=65, default="000")
    Account_ID = models.CharField(max_length=65, verbose_name="Account_Number")
    Account_Name = models.CharField(max_length=500)
    LCY_Amount = models.FloatField(null=True, blank=True)
    LCY_Code = models.CharField(max_length=10,default=None, choices=LCY_Codes, null=True, blank=True)
    FCY_Amount = models.IntegerField(null=True, blank=True)
    FCY_Code = models.CharField(max_length=20, null=True, blank=True)
    Trans_Code = models.CharField(max_length=45, default=None, choices=Trans_Codes, null=True, blank=True)
    Trans_Mode = models.CharField(max_length=100, default=None, null=True, blank=True)
    Cheque_No = models.CharField(max_length=35,default=None, null=True, blank=True)
    Narrative = models.CharField(max_length=500,default=None, blank=True)

    Value_Date = models.DateTimeField(null=True, blank=True)
    Booking_Date = models.DateTimeField(null=True, blank=True)
    Posting_Date = models.DateTimeField(null=True, blank=True)

    Entry_Date = models.DateTimeField(default=timezone.now, blank=True)
    ENTRY_TIME = models.DateTimeField(null=True, blank=True)

    IC4_Account_Officer = models.CharField(max_length=35, null=True, blank=True)
    IC4_Inputter = models.CharField(max_length=50, null=True, blank=True)
    IC4_Authoriser = models.CharField(max_length=50, null=True, blank=True)
    IC4_Verifier = models.CharField(max_length=35, null=True, blank=True)

    Text_Field_1 = models.CharField(max_length=65, null=True, blank=True)
    Text_Field_2 = models.CharField(max_length=65, null=True, blank=True)
    AMT_Field_1 = models.FloatField(null=True, blank=True)
    AMT_Field_2 = models.IntegerField(null=True, blank=True)
    Date_Field_1 = models.DateTimeField(null=True, blank=True)
    Date_Field_2 = models.DateTimeField(null=True, blank=True)

    Callover_Remark = models.CharField(max_length=100, null=True, blank=True)
    Exception_Id  = models.CharField(max_length=65, null=True, blank=True)
    Severity_Id = models.CharField(max_length=65, null=True, blank=True)
    Review_Date = models.DateTimeField(null=True, blank=True)

    Callover_Officer = models.CharField(max_length=120, null=True, blank=True)
    Callover_Date = models.DateTimeField(null=True, blank=True)
    Callover_Time = models.DateTimeField(null=True, blank=True)

    IC4_Special = models.CharField(max_length=35 , null=True, blank=True)
    # IP_Address = models.CharField(max_length=20, null=True, blank=True, default='127.0.0.1:8090')
    IP_Address = models.CharField(max_length=20, null=True, blank=True)
    Checker_ID = models.CharField(max_length=100 , null=True, blank=True)
    Checker_Date_Time = models.DateTimeField(null=True, blank=True)
    Callover_ID = models.CharField(max_length=100 , null=True, blank=True)

    Post_BRN =models.CharField(max_length=65, null=True, blank=True)
    Batch_No =models.CharField(max_length=65, null=True, blank=True)
    V_Num =models.CharField(max_length=65, null=True, blank=True)
    Doc_No =  models.CharField(max_length=20, null=True, blank=True)
    DR_TXN_NGN = models.IntegerField(null=True, blank=True)
    RATE  = models.IntegerField(null=True, blank=True)

    TXN_MNEM = models.CharField(max_length=20, null=True, blank=True)
    AC_GL_BRN_Name = models.CharField(max_length=65, null=True, blank=True)
    Cod_Bank = models.CharField(max_length=20, null=True, blank=True)
    TXN_Mnemonic = models.CharField(max_length=65, null=True, blank=True)
    TXN_Branch = models.CharField(max_length=20, null=True, blank=True)

    Amount = models.IntegerField(null=True, blank=True)
    Time_Key = models.IntegerField(null=True, blank=True)
    Tran_Date = models.DateTimeField(null=True,blank=True)

    Module = models.CharField(max_length=65, null=True, blank=True)
    Customer_No = models.CharField(max_length=65, null=True, blank=True)
    Settle_AC  = models.CharField(max_length=65, null=True, blank=True)
    Maturity_Date = models.DateTimeField(null=True, blank=True)
    Principal_Outstanding_Bal = models.IntegerField(null=True, blank=True)

    Product_Code = models.CharField(max_length=65, null=True, blank=True)
    Product_Name = models.CharField(max_length=200, null=True, blank=True)
    Product_Desc = models.CharField(max_length=100, null=True, blank=True)
    Product_Category = models.CharField(max_length=100, null=True, blank=True)
    Portfolio_ID = models.CharField(max_length=65, null=True, blank=True)
    Security_ID = models.CharField(max_length=65, null=True, blank=True)

    Price_Pct = models.IntegerField(null=True, blank=True)
    Buy_Sell = models.IntegerField(null=True, blank=True)
    Yield = models.IntegerField(null=True, blank=True)
    Nominal = models.IntegerField(null=True, blank=True)

    Validated = models.CharField(max_length=65, null=True, blank=True)
    Act_Price = models.IntegerField(null=True, blank=True)
    Perct_Coupon = models.IntegerField(null=True, blank=True)
    Comp_Mis_2 = models.CharField(max_length=65, null=True, blank=True)
    Tenor = models.CharField(max_length=65, null=True, blank=True)
    Application_Num = models.CharField(max_length=65, null=True, blank=True)
    Applicant_Name = models.CharField(max_length=100, null=True, blank=True)
    Remarks = models.CharField(max_length=500, null=True, blank=True)
    Status = models.CharField(max_length=20, null=True, blank=True)

    Start_Date = models.DateTimeField(null=True, blank=True)
    Expiry_Date = models.DateTimeField(null=True, blank=True)
    Cancellation_Date = models.DateTimeField(null=True, blank=True)

    Segment = models.IntegerField(null=True, blank=True)
    Interest = models.IntegerField(null=True, blank=True)
    Ins_Fee = models.IntegerField(null=True, blank=True)
    Proc_Charge = models.IntegerField(null=True, blank=True)
    Mgt_Fees = models.IntegerField(null=True, blank=True)

    Maker_Id = models.CharField(max_length=100, null=True, blank=True)
    Account_Class = models.CharField(max_length=65, null=True, blank=True)
    Account_Type = models.CharField(max_length=100, null=True, blank=True)
    Branch_Name = models.CharField(max_length=200, null=True, blank=True)
    Txn_Code = models.CharField(max_length=65, null=True, blank=True)
    Beneficiary_Bank = models.CharField(max_length=100, null=True, blank=True)
    Beneficiary_Name = models.CharField(max_length=200, null=True, blank=True)
    Beneficiary_Account = models.CharField(max_length=65, null=True, blank=True)
    Ref_Num = models.CharField(max_length=65, null=True, blank=True)


class IC4_ACCEPTED_CALLOVER(models.Model):
    class Meta:
        db_table='TMP_ACCEPTED_CALLOVER_L3'
    Tree_Key = models.IntegerField()
    CallOver_ID = models.CharField(max_length=100, unique=True)
    GRP_BY_REF = models.CharField(max_length=100, primary_key=True)
    GRP_BY_USER = models.CharField(max_length=100, null=True, blank=True)
    GRP_BY_DATE = models.DateTimeField(null=True, blank=True)
    Branch_Code = models.CharField(max_length=10, null=True, blank=True)
    Accepted_Date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    Ref_Num = models.CharField(max_length=100, null=True, blank=True)
    Callover_Officer = models.CharField(max_length=100, null=True, blank=True)

