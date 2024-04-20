from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from account.models import Profile
from quiz.models import UserRank, Quiz, Question, QuizSubmission
from django.contrib import messages
from .models import Message
import datetime
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.
def home(request):
    
    leaderboard_users = UserRank.objects.order_by('rank')[:6]
    
    if request.user.is_authenticated:
         #request user
         user_object2 = User.objects.get(username=request.user)
         user_profile2 = Profile.objects.get(username=user_object2)
         context = {"user_profile2":user_profile2, "leaderboard_users": leaderboard_users}
    else:
        context = {"leaderboard_users": leaderboard_users}
    
    return render(request, 'homepage.html', context)

@login_required(login_url='login')
def leaderboard_view(request):
    
    leaderboard_users = UserRank.objects.order_by('rank')
    
    user_object2 = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(username=user_object2)
    
    context = {"user_profile2": user_profile2, "leaderboard_users": leaderboard_users}
    return render(request, 'leaderboard.html', context)


def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
@login_required(login_url='login')
def dashboard_view(request):
    
    user_object2 = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(username=user_object2)
    
    #total number
    total_users = User.objects.all().count()
    total_quizzes = Quiz.objects.all().count()
    total_quiz_submit = QuizSubmission.objects.all().count()
    total_questions = Question.objects.all().count()
    
    #todays number 
    today_users = User.objects.filter(date_joined__date=datetime.date.today()).count()
    today_quizzes_objs = Quiz.objects.filter(created_at__date=datetime.date.today())
    today_quizzes = Quiz.objects.filter(created_at__date=datetime.date.today()).count()
    today_quiz_submit = QuizSubmission.objects.filter(submitted_at__date=datetime.date.today()).count()
    today_questions = 0
    for quiz in today_quizzes_objs:
        today_questions += quiz.question_set.count()
    
    #gain
    gain_users = gain_percent(total_users, today_users)
    gain_quizzes = gain_percent(total_quizzes, today_quizzes)
    gain_quiz_submit = gain_percent(total_quiz_submit, today_quiz_submit)
    gain_questions = gain_percent(total_questions, today_questions)
    
    #inbox
    messages = Message.objects.filter(created_at__date=datetime.date.today()).order_by('-created_at')
    
    context = {"user_profile2": user_profile2,
               "total_users": total_users,
               "total_quizzes": total_quizzes,
               "total_quiz_submit": total_quiz_submit, "total_questions": total_questions,
               "today_users": today_users, "today_quizzes": today_quizzes,
               "today_quiz_submit": today_quiz_submit, "today_questions": today_questions,
               "gain_users": gain_users, "gain_quizzes": gain_quizzes, "gain_quiz_submit": gain_quiz_submit,
               "gain_questions": gain_questions, "messages": messages,}
    return render(request, "dashboard.html", context)

def gain_percent(total, today):
    gain = 0
    if total > 0 and today > 0:
        gain = (today*100)/total
    return gain


def about_view(request):
    
    if request.user.is_authenticated:
        user_object2 = User.objects.get(username=request.user)
        user_profile2 = Profile.objects.get(username=user_object2)
        context = {"user_profile2": user_profile2}
    else:
        context = { }   
    return render(request, 'about.html', context)

def contact_view(request):
    
    user_object2 = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(username=user_object2)
    
    if request.method == "POST":
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        if subject is not None and message is not None:
            form  = Message.objects.create(user=request.user, subject=subject, message=message)
            form.save()
            messages.success(request, "We recieve your message. we'll revert you soon")
            return redirect('contact')
        else:
            return redirect('contact')
        
    context = {"user_profile2": user_profile2}
    return render(request, 'contact.html', context)

@user_passes_test(is_superuser)
@login_required(login_url='login')
def message_view(request, id):
    
    user_object2 = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(username=user_object2)
    
    message = Message.objects.filter(id=int(id)).first()
    if not message.is_read:
        message.is_read = True
        message.save()
    
    context = {"user_profile2": user_profile2, "message": message}
    return render(request, "message.html", context)

def terms_conditions_view(request):
    
    if request.user.is_authenticated:
         #request user
         user_object2 = User.objects.get(username=request.user)
         user_profile2 = Profile.objects.get(username=user_object2)
         context = {"user_profile2":user_profile2}
    else:
        context = { }
    return render(request, 'terms.html', context)

def search_users_view(request):
    
    query = request.GET.get('q')
    
    if query:
        users = User.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query)
        ).order_by('date_joined')
    else:
        users = []
    
    if request.user.is_authenticated:
        user_object2 = User.objects.get(username=request.user)
        user_profile2 = Profile.objects.get(username=user_object2)
        context = {"user_profile2": user_profile2, "query": query, "users": users}
    else:
        context = {"query": query, "users": users}
    return render(request, "search-users.html", context)