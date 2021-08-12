from django import forms
from .models import Book,Employee
#DataFlair
class BookCreate(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
class EmpCreate(forms.ModelForm):
    class Meta:
        model=Employee
        fields='__all__'

# class TranCreate(forms.ModelForm):
#     class Meta:
#         model=Transection
#         fields='__all__'