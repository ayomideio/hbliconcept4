import random

from django.db import models
from django.contrib.auth.models import User


#DataFlair Models
from django.utils import timezone


class Book(models.Model):
    name = models.CharField(max_length = 50)
    picture = models.ImageField()
    author = models.CharField(max_length = 30)
    email = models.EmailField(blank = True)
    describe = models.TextField()
    def __str__(self):
        return self.name

class Employee(models.Model):
    id = models.CharField(primary_key=True,max_length=20)
    UserName=models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    Branch_Code=models.CharField(max_length=100)
    Entry_date=models.DateTimeField(default=timezone.now)
    Entry_User_ID= models.CharField(max_length=100)
    NO_OF_ENTRIES=models.FloatField(default=0.0)
    CREDIT_FREQ=models.FloatField(default=0.0)
    TOTAL_CREDIT=models.FloatField(default=0.0)
    DEBIT_FREQ=models.FloatField(default=0.0)
    TOTAL_DEBIT=models.FloatField(default=0.0)
    eemail = models.EmailField()
    econtact = models.CharField(max_length=15)


# class EmployeeeName(models.Model):

    # class Meta:
    #     db_table = "employee"

class Branch(models.Model):
    Branch_ID = models.IntegerField()
    Branch_Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Branch_Name

class Profile(models.Model):
    class Meta:
        db_table='PROFILE'
    Profile_ID = models.CharField(max_length=20, unique=True, null=True, blank=True)
    Title = models.IntegerField(default=00, null=True, blank=True)
    User_Name = models.CharField(max_length=100)
    Email = models.EmailField()
    Special_Emails = models.EmailField(null=True, blank=True)
    Mobile_Number = models.IntegerField()
    Branch_code = models.ForeignKey(Branch, on_delete=models.CASCADE, default=None)
    Department = models.IntegerField()
    Profile_Comment = models.CharField(max_length=250)
    Date_Created = models.DateTimeField(null=True, blank=True)
    Created_By = models.IntegerField()
    Modified_Date = models.DateTimeField(null=True, blank=True)
    Modified_By = models.IntegerField()

    def __str__(self):
        return self.User_Name

Account_Choices = (
    ('Current', 'CURRENT'),
    ('Saving', 'SAVING'),
    ('Salary', 'SALARY'),
    ('Student', 'STUDENT'),
)


def random_string():
    str1 = str(random.randint(1000, 9999))
    str2 = str(random.randint(1000, 9999))
    str3 = str(random.randint(1000, 9999))
    str4 = str(random.randint(1000, 9999))
    acc_num = str1 + "-" + str2 + "-" + str3 + "-" + str4

    return acc_num

class Account(models.Model):
    Account_Name = models.CharField(max_length=500)
    Account_Num = models.CharField(max_length=65, default=random_string, verbose_name="Account_Number")
    Account_Type = models.CharField(max_length=20, choices=Account_Choices,default=None)
    Profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.Account_Name




class CallOver_Detail(models.Model):
    Callover_officer = models.CharField(max_length=120, null=True, blank=True)
    Callover_date = models.DateTimeField(null=True, blank=True)
    Callover_time = models.TimeField(null=True, blank=True)
    Callover_remark = models.CharField(max_length=100, null=True, blank=True)

class Beneficiary_Details(models.Model):
    Branch_Name = models.CharField(max_length=100, default=None, null=True, blank=True)
    Beneficiary_Bank = models.CharField(max_length=50, default=None, null=True, blank=True)
    Beneficiary_Name = models.CharField(max_length=100, default=None, null=True, blank=True)
    Beneficiary_account = models.CharField(max_length=100, default=None, null=True, blank=True)

Trans_Choices = (
    ('Credit', 'CREDIT'),
    ('Debit', 'DEBIT'),
)

LCY_Codes = (
    ('USD', 'USD'),
    ('NGN', 'NGN'),
)


Trans_Codes = (
    ('Credit','C'),
    ('Debit','D')
)
class UserRoles(models.Model):
    class Meta:
        db_table="User Role"
    id=models.AutoField(primary_key=True)
    User_Id=models.CharField(max_length=100)
    Group_Name=models.CharField(max_length=100)

class IC4_Callover(models.Model):
    class Meta:
        db_table='CALLOVER_TRANSACTION'
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
    Date_Field_2 = models.TimeField(null=True, blank=True)

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

class IC4_Callover_L3(models.Model):
    class Meta:
        db_table='CALLOVER_TRANSACTION_L3'
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


# class IC4_Callover_Waiting_L3(models.Model):
#     class Meta:
#         db_table='CALLOVER_WAITING_L3'
#     Trans_ID =  models.CharField(max_length=255, default="abc")
#     Trans_Ref_ID =  models.CharField(max_length=65)
#     Trans_Sub_ID =  models.CharField(max_length=245)
#     Branch_Code = models.CharField(max_length=65, default="000")
#     Account_ID = models.CharField(max_length=65, verbose_name="Account_Number")
#     Account_Name = models.CharField(max_length=500)
#     LCY_Amount = models.FloatField(null=True, blank=True)
#     LCY_Code = models.CharField(max_length=10,default=None, choices=LCY_Codes, null=True, blank=True)
#     FCY_Amount = models.IntegerField(null=True, blank=True)
#     FCY_Code = models.CharField(max_length=20, null=True, blank=True)
#     Trans_Code = models.CharField(max_length=45, default=None, choices=Trans_Codes, null=True, blank=True)
#     Trans_Mode = models.CharField(max_length=100, default=None, null=True, blank=True)
#     Cheque_No = models.CharField(max_length=35,default=None, null=True, blank=True)
#     Narrative = models.CharField(max_length=500,default=None, blank=True)

#     Value_Date = models.DateTimeField(null=True, blank=True)
#     Booking_Date = models.DateTimeField(null=True, blank=True)
#     Posting_Date = models.DateTimeField(null=True, blank=True)

#     Entry_Date = models.DateTimeField(default=timezone.now, blank=True)
#     ENTRY_TIME = models.TimeField(null=True, blank=True)

#     IC4_Account_Officer = models.CharField(max_length=35, null=True, blank=True)
#     IC4_Inputter = models.CharField(max_length=50, null=True, blank=True)
#     IC4_Authoriser = models.CharField(max_length=50, null=True, blank=True)
#     IC4_Verifier = models.CharField(max_length=35, null=True, blank=True)

#     Text_Field_1 = models.CharField(max_length=65, null=True, blank=True)
#     Text_Field_2 = models.CharField(max_length=65, null=True, blank=True)
#     AMT_Field_1 = models.FloatField(null=True, blank=True)
#     AMT_Field_2 = models.IntegerField(null=True, blank=True)
#     Date_Field_1 = models.DateTimeField(null=True, blank=True)
#     Date_Field_2 = models.TimeField(null=True, blank=True)

#     Callover_Remark = models.CharField(max_length=100, null=True, blank=True)
#     Exception_Id  = models.CharField(max_length=65, null=True, blank=True)
#     Severity_Id = models.CharField(max_length=65, null=True, blank=True)
#     Review_Date = models.DateTimeField(null=True, blank=True)

#     Callover_Officer = models.CharField(max_length=120, null=True, blank=True)
#     Callover_Date = models.DateTimeField(null=True, blank=True)
#     Callover_Time = models.DateTimeField(null=True, blank=True)

#     IC4_Special = models.CharField(max_length=35 , null=True, blank=True)
#     # IP_Address = models.CharField(max_length=20, null=True, blank=True, default='127.0.0.1:8090')
#     IP_Address = models.CharField(max_length=20, null=True, blank=True)
#     Checker_ID = models.CharField(max_length=100 , null=True, blank=True)
#     Checker_Date_Time = models.DateTimeField(null=True, blank=True)
#     Callover_ID = models.CharField(max_length=100 , null=True, blank=True)

#     Post_BRN =models.CharField(max_length=65, null=True, blank=True)
#     Batch_No =models.CharField(max_length=65, null=True, blank=True)
#     V_Num =models.CharField(max_length=65, null=True, blank=True)
#     Doc_No =  models.CharField(max_length=20, null=True, blank=True)
#     DR_TXN_NGN = models.IntegerField(null=True, blank=True)
#     RATE  = models.IntegerField(null=True, blank=True)

#     TXN_MNEM = models.CharField(max_length=20, null=True, blank=True)
#     AC_GL_BRN_Name = models.CharField(max_length=65, null=True, blank=True)
#     Cod_Bank = models.CharField(max_length=20, null=True, blank=True)
#     TXN_Mnemonic = models.CharField(max_length=65, null=True, blank=True)
#     TXN_Branch = models.CharField(max_length=20, null=True, blank=True)

#     Amount = models.IntegerField(null=True, blank=True)
#     Time_Key = models.IntegerField(null=True, blank=True)
#     Tran_Date = models.DateTimeField(null=True,blank=True)

#     Module = models.CharField(max_length=65, null=True, blank=True)
#     Customer_No = models.CharField(max_length=65, null=True, blank=True)
#     Settle_AC  = models.CharField(max_length=65, null=True, blank=True)
#     Maturity_Date = models.DateTimeField(null=True, blank=True)
#     Principal_Outstanding_Bal = models.IntegerField(null=True, blank=True)

#     Product_Code = models.CharField(max_length=65, null=True, blank=True)
#     Product_Name = models.CharField(max_length=200, null=True, blank=True)
#     Product_Desc = models.CharField(max_length=100, null=True, blank=True)
#     Product_Category = models.CharField(max_length=100, null=True, blank=True)
#     Portfolio_ID = models.CharField(max_length=65, null=True, blank=True)
#     Security_ID = models.CharField(max_length=65, null=True, blank=True)

#     Price_Pct = models.IntegerField(null=True, blank=True)
#     Buy_Sell = models.IntegerField(null=True, blank=True)
#     Yield = models.IntegerField(null=True, blank=True)
#     Nominal = models.IntegerField(null=True, blank=True)

#     Validated = models.CharField(max_length=65, null=True, blank=True)
#     Act_Price = models.IntegerField(null=True, blank=True)
#     Perct_Coupon = models.IntegerField(null=True, blank=True)
#     Comp_Mis_2 = models.CharField(max_length=65, null=True, blank=True)
#     Tenor = models.CharField(max_length=65, null=True, blank=True)
#     Application_Num = models.CharField(max_length=65, null=True, blank=True)
#     Applicant_Name = models.CharField(max_length=100, null=True, blank=True)
#     Remarks = models.CharField(max_length=500, null=True, blank=True)
#     Status = models.CharField(max_length=20, null=True, blank=True)

#     Start_Date = models.DateTimeField(null=True, blank=True)
#     Expiry_Date = models.DateTimeField(null=True, blank=True)
#     Cancellation_Date = models.DateTimeField(null=True, blank=True)

#     Segment = models.IntegerField(null=True, blank=True)
#     Interest = models.IntegerField(null=True, blank=True)
#     Ins_Fee = models.IntegerField(null=True, blank=True)
#     Proc_Charge = models.IntegerField(null=True, blank=True)
#     Mgt_Fees = models.IntegerField(null=True, blank=True)

#     Maker_Id = models.CharField(max_length=100, null=True, blank=True)
#     Account_Class = models.CharField(max_length=65, null=True, blank=True)
#     Account_Type = models.CharField(max_length=100, null=True, blank=True)
#     Branch_Name = models.CharField(max_length=200, null=True, blank=True)
#     Txn_Code = models.CharField(max_length=65, null=True, blank=True)
#     Beneficiary_Bank = models.CharField(max_length=100, null=True, blank=True)
#     Beneficiary_Name = models.CharField(max_length=200, null=True, blank=True)
#     Beneficiary_Account = models.CharField(max_length=65, null=True, blank=True)
#     Ref_Num = models.CharField(max_length=65, null=True, blank=True)




# class IC4_Profile(models.Model):
#     Profile_ID = models.CharField(max_length=20)
#     Title = models.CharField(max_length=10)
#     User_Name = models.CharField(max_length=100)
#     Email = models.EmailField()
#     Special_Email = models.EmailField(null=True, blank=True)
#     Mobile =  models.CharField(max_length=15)
#     Branch_Code = models.CharField(max_length=5)
#     Department = models.CharField(max_length=5)
#     Profile_Comment = models.CharField(max_length=150, null=True, blank=True)
#     Date_Created = models.DateTimeField(null=True,blank=True)
#     Created_By = models.CharField(max_length=30)
#     Modified_Date = models.DateTimeField(null=True, blank=True)
#     Modified_By = models.CharField(max_length=30)


class IC4_ACCEPTED_CALLOVER(models.Model):
    class Meta:
        db_table='TMP_ACCEPTED_CALLOVER'
        
    Tree_Key = models.IntegerField()
    CallOver_ID = models.CharField(max_length=100, unique=True)
    GRP_BY_REF = models.CharField(max_length=100, primary_key=True)
    GRP_BY_USER = models.CharField(max_length=100, null=True, blank=True)
    GRP_BY_DATE = models.DateTimeField(null=True, blank=True)
    Branch_Code = models.CharField(max_length=10, null=True, blank=True)
    Accepted_Date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    Ref_Num = models.CharField(max_length=100, null=True, blank=True)
    Callover_Officer = models.CharField(max_length=100, null=True, blank=True)

# class IC4_ACCEPTED_CALLOVER_L3(models.Model):
#     class Meta:
#         db_table='TMP_ACCEPTED_CALLOVER_L3'
        
#     Tree_Key = models.IntegerField(primary_key=True)
#     CallOver_ID = models.CharField(max_length=100, unique=True)
#     GRP_BY_REF = models.CharField(max_length=100, null=True, blank=True)
#     GRP_BY_USER = models.CharField(max_length=100, null=True, blank=True)
#     GRP_BY_DATE = models.DateTimeField(null=True, blank=True)
#     Branch_Code = models.CharField(max_length=10, null=True, blank=True)
#     Accepted_Date = models.DateTimeField(null=True, blank=True, default=timezone.now)
#     Ref_Num = models.CharField(max_length=100, null=True, blank=True)
#     Callover_Officer = models.CharField(max_length=100, null=True, blank=True)

class IC4_CALLOVER_EXCEPTION(models.Model):
    class Meta:
        db_table='CALLOVER_EXCEPTION'
    
    CallOver_ID = models.CharField(max_length=100)
    
    Branch_Code = models.CharField(max_length=65)
    
    
    Observation = models.CharField(max_length=105, blank=True, null=True)
    Severity_Level = models.CharField(max_length=65, blank=True, null=True)
    Issue_Priority = models.CharField(max_length=10, blank=True, null=True)
    Maturity_Rating = models.CharField(max_length=15, blank=True, null=True)
    Review = models.DateField(blank=True, null=True)
    Exception_Detail = models.CharField(max_length=100, blank=True, null=True)
    Implication = models.CharField(max_length=100, blank=True, null=True)
    Action = models.CharField(max_length=100, blank=True, null=True)
    Callover_Officer = models.CharField(max_length=100, blank=True, null=True)
    Callover_Date  = models.DateField()
    Tree_ID = models.IntegerField(blank=True, null=True)
    Checker_ID = models.CharField(max_length=100, blank=True, null=True)
    Checker_Date_Time = models.DateField(blank=True, null=True)
    IC4_Severity_Level_ID = models.CharField(max_length=20, blank=True, null=True)
    Owner_Name = models.CharField(max_length=200, blank=True, null=True)
    Owner_Detail = models.CharField(max_length=200, blank=True, null=True)
    Alert_Comments = models.CharField(max_length=500, blank=True, null=True)
    Accepted_By = models.CharField(max_length=500, blank=True, null=True)
    Accepted_Date = models.DateField(blank=True, null=True)
    Other_Receivers = models.CharField(max_length=500, blank=True, null=True)
    Supervisor = models.CharField(max_length=500, blank=True, null=True)
    Exception_Status = models.CharField(max_length=200, blank=True, null=True)
    Callover_Level = models.CharField(max_length=100, blank=True, null=True)
    Inputter_Name = models.CharField(max_length=200, blank=True, null=True)
    Inputter_Email = models.CharField(max_length=100, blank=True, null=True)


class IC4_Observation_Model(models.Model):
    class Meta:
        db_table='OBSERVATION_MODEL'
    ID = models.AutoField(primary_key=True)
    Description = models.CharField(max_length=500, blank=True, null=True)
    User_Comments = models.CharField(max_length=500, blank=True, null=True)
    Severity_Level = models.CharField(max_length=500, blank=True, null=True)
    Implication = models.CharField(max_length=500, blank=True, null=True)
    Action = models.CharField(max_length=500, blank=True, null=True)





