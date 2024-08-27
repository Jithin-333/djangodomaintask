from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache,cache_control
from django.contrib import messages


@never_cache
def login_view(request):
    if request.user.is_authenticated:
    # if 'username' in request.session:
         return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # request.session['username']= username
            login(request, user)
            if request.user.is_authenticated:
                return redirect('home')
            
        
        # form is invalid it provide a error message
        error_message = "Invalid username or password."
        return render(request, 'login.html', {'error_message': error_message})
    
    return render(request, 'login.html')

@never_cache
# @login_required(login_url='/')
def logout_view(request):
    if request.user.is_authenticated:
    # if 'username' in request.session:
        # request.session.flush()
        logout(request)
    return redirect('login')

@never_cache 
# @login_required(login_url='/')
def home_view(request):
    if request.user.is_authenticated:       
        if request.user.is_superuser:
            return redirect("admin_home")
        return render(request,'homepage.html') 
       
    return redirect('login')  


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')

        if pass1 != pass2:
            messages.warning(request, "password not matching")
            return redirect(register)
        
        if User.objects.filter(username=uname).exists():
            messages.warning(request, "User name is already taken!")
            return redirect(register)
        
        if User.objects.filter(email=email).exists():
            messages.warning(request, "Email is already registered!")
            return redirect(register)
        if ' ' in  uname:
            messages.warning(request, "username can't contain spaces")
            return redirect(register)



        if len(pass1) < 8:
            messages.warning(request, "Password must be at least 8 characters")
            return redirect(register)

        if not (email.endswith('@gmail.com') and email[0].isalpha()):
            messages.warning(request, "Enter a valid email")
            return redirect(register)
        

        my_user = User.objects.create_user(uname,email,pass1)  
        my_user.save()
        return redirect('login')
          
    return render(request,'signin.html')

