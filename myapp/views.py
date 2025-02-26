from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

# from .models import Post
# Create your views here.
def home(request):
    return render(request, 'home.html')

def dashboard(request):
    return render(request, 'dashboard.html')
    # if request.user.is_authenticated:
    #     pass
    #     return render(request , 'dashboard.html')
    # else:
    # return HttpResponseRedirect('/user_login/')

def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out Successfully!')
    return HttpResponseRedirect('/') 


def user_signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()

    else:
        form = SignUpForm()
    return render(request , 'signup.html', {'form' : form})



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
                    return HttpResponseRedirect('/dashboard/') 
                return render(request, 'login.html')
        else:
            form = LoginForm()
        return render(request, 'login.html', {'form': form})
    else:
        return HttpResponseRedirect('/')