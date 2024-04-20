from django.shortcuts import render, redirect
from django.core.validators import validate_email
import re
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from . models import Profile
from quiz.models import QuizSubmission

# Create your views here.
def register(request):
    
    if request.method == "POST":
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        repeat_password = request.POST['repeat_password']
        
        #Password validation regex
        password_regex = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$')
        
        #Username validation regex
        username_regex = re.compile(r'^(?=.*[a-zA-Z])(?=.*\d*[a-zA-Z])\w{5,}$')
        
        #check if email is valid or not
        try:
            validate_email(email)
        except ValidationError:
            messages.info(request, "Enter your valid Email Address.")
            return redirect('register')
        
        #check if chosen username is valid
        if not username_regex.match(username):
            messages.info(request, """Username must contain at least 5 characters with alphabet or 
                          alphabet with a number, where the alphabet should be at least 4 characters 
                          if combined with a number.""")
        
        #check if chosen password is valid
        if not password_regex.match(password):
            messages.info(request, '''Password should contain at least 8 characters with at 
                          least one alphabet, number, and special character.''')
            return redirect('register')
        
        if password == repeat_password:
            #check if username available
            if User.objects.filter(username=username).exists():
                messages.info(request, "This username is not available.")
                return redirect('register')
            
            #check if email available
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Your email is already exists.")
                return redirect('register')
            
            #create user
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()     
                
                #login in the user and redirect to profile
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
                
                #create profile for new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(username=user_model)
                new_profile.save()
                return redirect('profile', username)
        else:
            messages.info(request, "Password unmatched.")
            return redirect('register')
    
    context = {}
    return render(request, "register.html", context)

@login_required(login_url='login')
def profile(request, username):
    #profile user
    user_object = User.objects.get(username=username)
    user_profile = Profile.objects.get(username=user_object)
    
    #request user
    user_object2 = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(username=user_object2)
    
    submissions = QuizSubmission.objects.filter(user=user_object)
    
    context = {"user_profile" : user_profile, "user_profile2" : user_profile2, "submissions": submissions}
    return render(request, "profile.html", context)


@login_required(login_url='login')
def editProfile(request):
    
    user_object2 = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(username=user_object2)
    
    if request.method == "POST":
        #image
        if request.FILES.get('profile_img')!=None:
            user_profile2.profile_img = request.FILES.get('profile_img')
            user_profile2.save()
            
        #username
        if request.POST.get('username')!=None:
            uname = User.objects.filter(username=request.POST.get('username')).first()
            
            if uname == None:
                user_object2.username = request.POST.get('username')
                user_object2.save()
            else:
                if uname != user_object2:
                    messages.info(request, "Username is already exits")
                    return redirect('edit_profile')
                
        #first and last name
        user_object2.first_name = request.POST.get('first_name')
        user_object2.last_name = request.POST.get('last_name')
        user_object2.save()
        
        #bio, gender, location
        user_profile2.bio = request.POST.get('bio')
        user_profile2.gender = request.POST.get('gender')
        user_profile2.location = request.POST.get('location')
        user_profile2.save()
        
        #email
        if request.POST.get('email')!=None:
            e = User.objects.filter(email=request.POST.get('email')).first()
            if e == None:
                user_object2.email = request.POST.get('email')
                user_object2.save()
            else:
                if e != user_object2:
                    messages.info(request, "Email is already exits")
                    return redirect('edit_profile')
        
        
        return redirect('profile', user_object2.username)
        
    
    context = {"user_profile2" : user_profile2}
    return render(request, "profile_edit.html", context)


def login(request):
    
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            return redirect('profile', username)
        else:
            messages.info(request,'Credentials invalid!')
    
    return render(request, "login.html")


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def deleteProfile(request):
    
    user_object2 = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(username=user_object2)
    
    if request.method == "POST" :
        user_profile2.delete()
        user_object2.delete()
        return redirect('logout')
    
    context = {"user_profile2" : user_profile2}
    return render(request, "profile_delete.html", context)
