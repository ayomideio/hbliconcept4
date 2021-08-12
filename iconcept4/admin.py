from django.contrib import admin
from .models import *
from django_reverse_admin import ReverseModelAdmin



class EmpAdmin(admin.ModelAdmin):
    list_display = ('id','Entry_User_ID','NO_OF_ENTRIES','CREDIT_FREQ','TOTAL_CREDIT','DEBIT_FREQ','TOTAL_DEBIT')

class AccountInline(admin.StackedInline):
    model = Account
    extra = 1

class ProfileAdmin(admin.ModelAdmin):
    inlines = [AccountInline]
    list_display = ('Profile_ID','Title','User_Name','Email','Branch_code','Department')

class BranchAdmin(admin.ModelAdmin):
    list_display = ('Branch_ID','Branch_Name')

class ProfileInline(admin.StackedInline):
    model = Profile
    # model = IC4_Profile

class AccountAdmin(ReverseModelAdmin):
    list_display = ('Account_Name', 'Account_Num')
    inline_type = 'stacked'
    inline_reverse = ['Profile_id']
    readonly_fields = ('Account_Num',)


class CallOverInline(admin.StackedInline):
    model = CallOver_Detail


class TransectionAdmin(ReverseModelAdmin):
    list_display = ('Trans_ID','Entry_User_id','Brach_code','LCY_Amount','Entry_Date','Trans_Type')
    fields = ('Entry_User_id','Trans_ID','Brach_code','Account_id','LCY_Amount','Trans_Type')

    inline_type = 'stacked'
    inline_reverse = []

class CalloverAdmin(admin.ModelAdmin):
    list_display = ['Trans_ID','Branch_Code','Entry_Date','Account_ID','Account_Name','LCY_Amount','IP_Address']

admin.site.register(Book)
admin.site.register(Employee,EmpAdmin)
admin.site.register(Profile,ProfileAdmin) 
# admin.site.register(IC4_Profile,ProfileAdmin)
admin.site.register(Branch,BranchAdmin)
admin.site.register(Account,AccountAdmin)
# admin.site.register(Transection,TransectionAdmin)


admin.site.register(IC4_Callover,CalloverAdmin)

