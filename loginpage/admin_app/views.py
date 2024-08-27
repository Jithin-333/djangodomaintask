from django.shortcuts import render,redirect,get_object_or_404    # type: ignore
from django.contrib import messages # type: ignore
from django.contrib.auth.models import User  # type: ignore
from django.db.models import Q      # type: ignore
#from django.contrib.auth.hashers import make_password
from django. views. decorators. cache import never_cache,cache_control # type: ignore

# Create your views here.
# ~~~~~~~~~~~~ADMIN_HOME~~~~~~~~~#
@never_cache
def admin_home(request): 
    if request.user.is_superuser:
        user = User.objects.all().order_by ('date_joined')
        return render(request, 'admin_home.html',{'users' : user})
    return redirect('home')


# ~~~~~~~~~~~CREATING_USER_FUNCTION~~~~~~~~~~~~~#
def create_user(request):
    if request.method == 'POST':
        user = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        password = request.POST.get('password')
        confirm_pass =request.POST.get('confirm_password')

        try:
            if User.objects.get(username=user):
                messages.warning(request, "User name is already taken")
                return redirect(admin_home)
        except User.DoesNotExist:
            pass

        try:
            if User.objects.get(email=user_email):
                messages.warning(request, "Email is Already Registered")
                return redirect(admin_home)
        except User.DoesNotExist:
            pass

        if password != confirm_pass:
            messages.warning(request, "Password doesn't match")
            return redirect(admin_home)
        
        if ' ' in  user:
            messages.warning(request, "username can't contain spaces")
            return redirect(admin_home) 

        
        if len(password) < 8:
            messages.warning(request, "Password must be at least 8 characters")
            return redirect(admin_home)

        if not (user_email.endswith('@gmail.com') and user_email[0].isalpha()):
            messages.warning(request, "Enter a valid email")
            return redirect(admin_home)

        user_details = User.objects.create_user(username=user,email = user_email,password=password)
        user_details.save()
        return redirect(admin_home)
    
    
# ~~~~~~~~~~~~~~~~DELETE_FUNCTION~~~~~~~~~~~~~~~~~~#
@never_cache
def delete_user(request,id):
    if request.method == "POST" and User.objects.filter(is_superuser=False):
        del_user = User.objects.get(id=id)
        del_user.delete()
        a = User.objects.filter(is_superuser=True)
        user = User.objects.all().order_by('username')
    return redirect(admin_home)
    # return render(request,'admin_home.html',{'users':user,'a':a})
  
    
# ~~~~~~~~~~~~~~~~~SEARCH_FUNCTION~~~~~~~~~~#
@never_cache
def admin_search(request):
    
    if request.method == "POST":
        user_details = request.POST.get('search')
        if user_details:
            user = User.objects.filter(username__icontains=user_details).order_by('username')
        else:
            user = User.objects.all()  
        return render(request,'admin_home.html',{'users':user})

# ~~~~~~~~~~~~~~EDIT_FUNCTION~~~~~~~~~~~~~~~~~#
def edit_user(request,id):
    user = get_object_or_404(User,id = id)
    if request.method == "POST":
        # user = User.objects.get(id = id)
        name = request.POST.get('username')
        email = request.POST.get('user_email')
        # password = request.POST['password']
        # confirm_pass = request.POST['confirm_password']

        try:
            if User.objects.filter(~Q(id = id),email = email).get():
                messages.warning(request,"email is taken")
                return redirect (admin_home)
        except:
            pass
        try:
            if User.object.get(username = name):
                messages.warning(request,"username is taken")
                return redirect(admin_home)
        except:
            pass
        if not (email.endswith('@gmail.com') and email[0].isalpha()):
            messages.warning(request, "Enter a valid email")
            return redirect(admin_home)
        if ' ' in  name:
            messages.warning(request, "username can't contain spaces")
            return redirect(admin_home)

        # if len(password) < 8:
        #     messages.success(request,'password min length 8')
        #     return redirect(admin_home)
        # if password == confirm_pass:
        #     user.password = make_password(password)
        # else:
            # messages.success(request,"passworrd doesn't match")
            # return redirect(admin_home)
        user.username = name
        user.email = email
        user.save()
        return redirect(admin_home)