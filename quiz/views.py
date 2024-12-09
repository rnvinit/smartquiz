from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .models import Question, Choice, UserProgress, QuizAttempt
import random

@require_http_methods(["GET"])
def home(request):
    return render(request, 'home.html')

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, f"Welcome, {username}! Your account has been created successfully.")
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

@login_required
@require_http_methods(["GET", "POST"])
def quiz(request):
    # Fetch or create the user's progress
    progress, created = UserProgress.objects.get_or_create(user=request.user)
    
    total_questions = 5  # Total number of questions per quiz

    # Reset score for new quiz attempt
    if request.method == 'POST':
        if progress.current_question_index == 0:  # Reset score only at the start of a new quiz
            progress.score = 0
        
        # Process current question submission
        question_id = int(request.POST.get('question_id'))
        selected_choice_id = int(request.POST.get('answer'))
        question = Question.objects.get(id=question_id)
        selected_choice = Choice.objects.get(id=selected_choice_id)

        # Real-time feedback based on the correctness of the answer
        if selected_choice.is_correct:
            messages.success(request, "Correct! Well done.")
            progress.score += 1  # Increment score for correct answer
        else:
            messages.error(request, "Incorrect! Try harder next time.")

        # Update user's progress and level
        progress.current_question_index += 1
        progress.level = progress.score // 10 + 1  # Increase level every 10 points
        progress.save()

        # Check if the user has completed the quiz
        if progress.current_question_index >= total_questions:
            # Save final quiz attempt
            QuizAttempt.objects.create(user=request.user, score=progress.score)
            messages.success(request, f"Quiz completed! Your score: {progress.score}/{total_questions}")
            
            # **Add current quiz score to total score**
            progress.total_score += progress.score
            progress.current_question_index = 0  # Reset the current question index for the next quiz
            progress.save()

            return redirect('result')

    # Fetch the next question based on the user's level and progress
    all_questions = Question.objects.filter(difficulty__lte=progress.level)
    if all_questions.exists():
        current_question = all_questions[progress.current_question_index % len(all_questions)]
        return render(request, 'quiz.html', {
            'question': current_question,
            'question_number': progress.current_question_index + 1,
            'total_questions': total_questions
        })
    else:
        messages.error(request, "No questions available at your level.")
        return redirect('home')

@login_required
@require_http_methods(["GET"])
def result(request):
    latest_attempt = QuizAttempt.objects.filter(user=request.user).order_by('-date').first()
    progress = UserProgress.objects.get(user=request.user)

    # **Leaderboard ordered by cumulative total_score**
    leaderboard = UserProgress.objects.order_by('-total_score')[:10]

    return render(request, 'result.html', {
        'score': latest_attempt.score if latest_attempt else 0,
        'total_score': progress.total_score,  # Cumulative total score
        'level': progress.level,
        'leaderboard': leaderboard  # Updated leaderboard with cumulative scores
    })

@require_http_methods(["GET"])
def about(request):
    return render(request, 'about.html')

def custom_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('home')
