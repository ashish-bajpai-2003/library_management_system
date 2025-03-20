
from django import forms
from .models import Book , Comment, BookRating , BorrowRecord
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    password1 = forms.CharField(label= 'Password')
    password2 = forms.CharField(label= 'Confirm Password(again)')
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2']
        labels = {'first_name' : 'First Name' , 'last_name' : 'Last Name'}

class LoginForm(forms.Form):
    Name = forms.CharField(max_length=20 , required=True)
    Password = forms.CharField()


class Usercomment(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['text']
        labels={'text':'Comment'}
        widgets={'text':forms.Textarea(attrs={'class': 'form-control'})}


class RatingForm(forms.ModelForm):
    class Meta:
        model = BookRating
        fields=['rating']


class Borrowform(forms.ModelForm):
    class Meta:
        model=BorrowRecord
        fields=['book','return_date','due_date']
        widgets={
                'book': forms.Select(attrs={'class': 'form-control'}),
                'return_date':forms.TextInput(attrs={'class':'form-control'}),
               'due_date':forms.TextInput(attrs={'class':'form-control'}),
        }
    