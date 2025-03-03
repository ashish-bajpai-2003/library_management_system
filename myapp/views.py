from django.shortcuts import render, HttpResponseRedirect , redirect
from .forms import SignUpForm, LoginForm , BorrowBookForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.db.models import Q
from .models import Book, Borrow
from django.utils import timezone
from .forms import BookAddForm

# from .models import Post
# Create your views here.
def home(request):
    return render(request, 'home.html')

# from django.shortcuts import render, redirect
# from .forms import BorrowBookForm
# from .models import Book, Borrow
# from django.contrib import messages

# def dashboard(request):
#     if request.user.is_authenticated:
#         if request.method == 'POST':
#             search_query = request.POST.get('q', '')
#             books = Book.objects.filter(book_name__icontains=search_query)  # Search by book name
#             if books.exists():
#                 # Display books that match search criteria
#                 return render(request, 'dashboard.html', {'books': books, 'form': BorrowBookForm()})
#             else:
#                 messages.error(request, "No books found matching your query.")
#                 return redirect('/dashboard/')
        
#         # Initially displaying an empty form on dashboard
#         return render(request, 'dashboard.html', {'form': BorrowBookForm()})
#     else:
#         return redirect('/user_login/')
def dashboard(request):
    if request.user.is_authenticated:
        books = Book.objects.filter(is_borrowed = False)
        return render(request,'dashboard.html',{'books' : books})
    
    else:
        return HttpResponseRedirect('/user_login/')


def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out Successfully!')
    return HttpResponseRedirect('/') 


# def user_signup(request):
#     if request.method == "POST":
#         form = SignUpForm(request.POST)
#         if form.is_valid():
#             user = form.save()

#     else:
#         form = SignUpForm()
#     return render(request , 'signup.html', {'form' : form})

def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Your account has been created successfully!')
            return HttpResponseRedirect('/user_login/')  # Redirect to login page after successful signup
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})




from django.contrib import messages

# def user_login(request):
#     if not request.user.is_authenticated:
#         if request.method == "POST":
#             form = LoginForm(request=request, data=request.POST)
#             if form.is_valid():
#                 uname = form.cleaned_data['username']
#                 upass = form.cleaned_data['password']
#                 user = authenticate(username=uname, password=upass)
#                 if user is not None:
#                     login(request, user)
#                     messages.success(request, 'Logged in Successfully!')
#                     return HttpResponseRedirect('/dashboard/')
#                 else:
#                     messages.error(request, 'Invalid username or password.')
#             else:
#                 messages.error(request, 'Form is not valid.')
#         else:
#             form = LoginForm()
#         return render(request, 'login.html', {'form': form})
#     else:
#         return HttpResponseRedirect('/')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged in Successfully!')
                    return HttpResponseRedirect('/dashboard/')  # Redirect to dashboard after successful login
                else:
                    messages.error(request, 'Invalid username or password.')
            else:
                messages.error(request, 'Form is not valid.')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        return HttpResponseRedirect('/')  # If already logged in, redirect to home



    

def search_books(request):
    query = request.GET.get('q','')
    if query:
        books = Book.objects.filter(
            Q(book_name__icontains=query) | Q(authors__author_name__icontains=query) | Q(book_publish_year__icontains = query)
        ).distinct()
    else:
        books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books, 'query': query})



def borrow_book(request, book_id):
    book = Book.objects.get(id=book_id)

    if request.method == 'POST':
        # book.is_borrowed = True
        borrow = Borrow(book=book, user=request.user)
        borrow.save()

        messages.success(request, f"You have borrowed {book.book_name} successfully!")
        book.delete()
        return redirect('/dashboard/')

    return render(request, 'borrow_book.html', {'book': book})

def return_book(request, borrow_id):
    borrow = Borrow.objects.get(id=borrow_id)
    borrow.return_date = timezone.now()
    borrow.save()

    messages.success(request, f"You have successfully returned {borrow.book.name}.")
    return HttpResponseRedirect('/dashboard/')


def add_book(request):
    if request.method == "POST":
        form = BookAddForm(request.POST)
        if form.is_valid():
            book = form.save(commit =False)
            book.save()
            book.authors.set(form.cleaned_data['authors'])  
            messages.success(request, "Book added successfully!")
            return redirect('add_book')  
    else:
        form = BookAddForm()
    return render(request, 'add_book.html', {'form': form})


def delete_book(request, book_id):
    book = Book.objects.get(id=book_id)
    book.delete()  
    messages.success(request, f"Book '{book.book_name}' deleted successfully!")
    return redirect('dashboard') 
