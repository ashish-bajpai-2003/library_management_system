from django.shortcuts import render , redirect , HttpResponse , HttpResponseRedirect , get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from .forms import  CustomUserCreationForm , LoginForm , RatingForm, Borrowform
from django.contrib import messages
from .models import Book, Comment , User , BookIssue
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login as django_login

# Create your views here.
def home(request):
    return render(request , 'home.html')

def search_books(request):
    query = request.GET.get('q', '')
    if query:
        books = Book.objects.filter(
            Q(book_name__icontains=query) |
            Q(authors__author_name__icontains=query) |
            Q(publish_date__icontains=query))
    else:
        books = Book.objects.all()

    return render(request, 'search_books.html', {'books': books, 'query': query})



def signup(request):
    if request.method == "POST":
        form =  CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save() 
            messages.success(request, "Your account has been created successfully!")
            return redirect('user_login') 
    else:
        form =  CustomUserCreationForm()  

    return render(request, 'signup.html', {'form': form})

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Name']
            password = form.cleaned_data['Password']
            
        
            user = authenticate(request, username=username, password=password)
            if user is not None:
                django_login(request, user)
           
                messages.success(request, "You logged in successfully!")
                
         
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})



def dashboard(request):
    return render(request , 'dashboard.html')


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})



def addcomment(request, id):
    book = Book.objects.get(pk=id)
    comments = book.comment_set.all()  
    if request.method == "POST":
        text = request.POST.get("text", "").strip()

        if text:  
            Comment.objects.create(book=book, user=request.user, text=text)
            return redirect('comment', id=book.id)  
    
    return render(request, 'comment.html', {'alldata': comments, 'book': book})



def book_like(request, id):
    book = Comment.objects.get(pk=id)
    if request.user.is_authenticated:
        if request.user not in book.likes.all():
            book.likes.add(request.user)
        else:
            book.likes.remove(request.user)

    return redirect('comment', id=book.book.id)

def user_logout(request):
    logout(request) 
    return HttpResponse('/') 

# from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, BookRating
from .forms import RatingForm
from django.contrib import messages


def rate_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    existing_rating = BookRating.objects.filter(book=book, user=request.user).first()

    if request.method == 'POST':
        form = RatingForm(request.POST)

        if form.is_valid():
            if existing_rating:
                existing_rating.rating = form.cleaned_data['rating']
                existing_rating.save()
                messages.success(request, "Your rating has been updated.")
            else:
                rating = form.save(commit=False)
                rating.book = book
                rating.user = request.user
                rating.save()
                messages.success(request, "Your rating has been submitted.")

            return redirect('book_detail', pk=book.id)

    else:
        initial_data = {'rating': existing_rating.rating} if existing_rating else {}
        form = RatingForm(initial=initial_data)

    return render(request, 'rate_book.html', {'book': book, 'form': form})


def deletecomment(request, id):
    pi = get_object_or_404(Comment, id=id)
    if request.user.is_superuser or request.user == pi.user:
        pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponse("You are not allowed to delete this comment.", status=403)
    

def issue_book(request,book_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to logged in to issue a book')
        return redirect('user_login')
    
    book = Book.objects.filter(id=book_id).first()

    if not book:
        messages.error(request, 'Book not found.')
        return redirect('book_detail')
    
    if book.available_copies > 0:
        BookIssue.objects.create(
            book=book,
            user= request.user
        )

        book.available_copies -= 1
        book.save()

        messages.success(request,'f{book.book_name} has been successfully issued!')
    else:
        messages.error(request,'Sorry, no copies of this book are available right now.')
    
    return redirect('book_list')

def book_list(request):
    books = Book.objects.all()
    return render(request,'book_list.html',{'books':books})


def return_book(request, book_id):
    if not request.user.is_authenticated:
        messages.error(request, 'You need to log in to return a book.')
        return redirect('user_login')

    book = Book.objects.filter(id=book_id).first()

    if not book:
        messages.error(request, 'Book not found.')
        return redirect('book_list')


    existing_issue = BookIssue.objects.filter(book=book, user=request.user, is_returned=False).first()

    if existing_issue:
   
        existing_issue.returned = True
        existing_issue.save()

        book.available_copies += 1
        book.save()

        messages.success(request, f'{book.book_name} has been successfully returned!')
    else:
        messages.error(request, 'You have not borrowed this book.')

    return redirect('book_list')



from .models import Book, BorrowRecord
from datetime import date
def borrow_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method=="POST":
        form=Borrowform(request.POST,instance=book)
        if form.is_valid():
            if book.available_copies > 0:
                borrow = BorrowRecord.objects.create(user=request.user, book=book)
                book.available_copies -= 1
                book.save()
                
                messages.success(request, f"You have borrowed '{book.book_name}'. Return by {borrow.due_date}.")
            else:
                messages.warning(request, "Sorry, this book is currently not available.")
    else:
        form=Borrowform()  
    return render(request,'borrow.html',{"form":form})


def return_book(request, borrow_id):
    borrow = get_object_or_404(BorrowRecord, id=borrow_id, user=request.user)

    if not borrow.is_returned:
        borrow.is_returned = True
        borrow.return_date = date.today()
        borrow.book.available_copies += 1
        borrow.book.save()
        borrow.save()

        messages.success(request, f"You have successfully returned '{borrow.book.book_name}'.")
    else:
        messages.warning(request, "This book is already returned.")

    return redirect('home')
