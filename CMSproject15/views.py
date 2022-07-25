from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.contrib import messages
# Create your views here.

def mode(request):
    if request.user.is_authenticated:
        mode = 'Logout'
    else:
        mode = 'Login'
        
    return mode

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, "Account successfully created")
                return redirect('login')

        context = {'form':form}
        return render(request, 'accounts/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, "Username or Password is incorrect")
        context = {}
        return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def home(request):
    context = {'mode':mode(request)}
    return render(request, 'accounts/home.html', context)

@login_required(login_url='login')
def dashboard(request):
    context = {'mode':mode(request)}
    return render(request, 'accounts/dashboard.html', context)

def newPage(request):
    file = open('newfile.html', 'w')