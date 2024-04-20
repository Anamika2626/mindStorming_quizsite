from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from account.models import Profile
from . models import Quiz, Category
from django.db.models import Q
from quiz.models import QuizSubmission
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def quiz_page(request):
    
    user_object2 = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(username=user_object2)
    
    quizzes = Quiz.objects.order_by('created_at')
    categories = Category.objects.all()
    
    context = {"user_profile2": user_profile2, "quizzes": quizzes, "categories": categories}                                 
    return render(request, 'quiz-page.html', context)

@login_required(login_url='login')
def search_view(request, category):
    
    user_object2 = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(username=user_object2)
    
    if request.GET.get('q') != None:  #search bar search
        q = request.GET.get('q')
        query = Q(title__icontains=q) | Q(description__icontains=q)
        quizzes = Quiz.objects.filter(query).order_by('created_at')
    elif category != " ":  #category search
        quizzes = Quiz.objects.filter(category__name=category).order_by('created_at')
    else:
        quizzes = Quiz.objects.order_by('created_at') 
               
    categories = Category.objects.all()
    
    context = {"user_profile2": user_profile2, "quizzes": quizzes, "categories": categories}
    return render(request, 'quiz-page.html', context)

@login_required(login_url='login')
def quiz_view(request, quiz_id):
    
    user_object2 = User.objects.get(username=request.user)
    user_profile2 = Profile.objects.get(username=user_object2)
    
    quiz = Quiz.objects.filter(id=quiz_id).first()
    total_questions = quiz.question_set.all().count()
    
    if request.method == "POST":
        
        #get the score
        score = int(request.POST.get('score', 0))
        
        #check if the user has already submitted the quiz
        if QuizSubmission.objects.filter(user=request.user, quiz=quiz).exists():
            messages.success(request, f"You got {score} out of {total_questions}")
            return redirect('quiz_view', quiz_id)
        
        #save the new quiz
        submission = QuizSubmission(user=request.user, quiz=quiz, score=score)
        submission.save()
        
        #show the result in messages
        messages.success(request, f"Quiz submitted successfully. You got {score} out of {total_questions}")
        return redirect('quiz_view', quiz_id)
        
            
    if quiz != None:
        context = {"user_profile2": user_profile2, "quiz": quiz}
    else:
        return redirect('quiz_page')
    return render(request, 'start-quiz-page.html', context)

