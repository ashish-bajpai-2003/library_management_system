from django import forms
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm , UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext , gettext_lazy as _
from .models import Borrow
from .models import Book , Author
# from .models import Post

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label = 'Password' , widget = forms.PasswordInput(attrs ={'class' : 'form-control'}))
    password2 = forms.CharField(label = 'Confirm Password(again)',  widget = forms.PasswordInput(attrs ={'class' : 'form-control'}))
    class Meta:
        model = User
        fields = ['username' , 'first_name' , 'last_name' , 'email']
        labels = {'first_name' : 'First Name' , 'last_name' : 'Last Name' , 'email' : 'Email'}
        widgets = {'username' :forms.TextInput(attrs={'class':'form-control'}),
                   'first_name':forms.TextInput(attrs={'class':'form-control'}),
                   'last_name' :forms.TextInput(attrs={'class':'form-control'}),
                   'email' : forms.TextInput(attrs={'class':'form-control'}),
        }


class LoginForm(AuthenticationForm):
    username = UsernameField(widget = forms.TextInput(attrs = {'autofocus' : True , 'class' : 'form-control'}))
    password = forms.CharField(label=_("Password"), strip = False ,widget = forms.PasswordInput(attrs={'autocomplete':'current-password' ,'class':'form-control'}))


class BorrowBookForm(forms.ModelForm):
    class Meta:
        model = Borrow
        fields = ['book' , 'due_date']



class BookAddForm(forms.ModelForm):
    authors = forms.CharField(widget = forms.TextInput(attrs={'class':'form-control','placefolder':'Enter authors name'}),
    help_text = 'Enter multiple authors by separeted by commas'
    )
    class Meta:
        model = Book    
        fields = ['book_name', 'authors', 'book_publish_year']



    def clean_authors(self):
    
            data = self.cleaned_data['authors']
            author_names = [name.strip() for name in data.split(',') if name.strip()]  

            if not author_names:
                raise forms.ValidationError("Please enter at least one author.")

            authors = []
            for name in author_names:
                author, created = Author.objects.get_or_create(author_name=name)  
                authors.append(author)  

            return authors