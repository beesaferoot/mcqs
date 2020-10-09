# import json
from django.forms import formset_factory, modelformset_factory
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import *
from .forms import QuizForm, QuestionForm, ChoiceForm


def index(request):
    context = {}
    return render(request, 'main/index.html', context)
    
def story(request):
    context = {'stories': Quiz.objects.all()}
    return render(request, 'main/story.html', context)

def dashboard(request):
    context = {'quizes': Quiz.objects.all()}
    return render(request, 'main/dashboard.html', context)

def assessment_instruction(request, id):
    quiz = Quiz.objects.get(pk=id)
    context = {'quiz': quiz}
    return render(request, 'main/instruction.html', context)

def assessment_results(request):
    assessments = Assessment.objects.filter(date_taken=datetime_safe.date.today())\
        .order_by('-start_time')[:5]
    context = {'assessments': assessments}
    return render(request, 'main/assessment_results.html', context)

def assessment_quiz(request, id):
    quiz = Quiz.objects.get(pk=id)
    if request.method == 'POST':
        data = request.POST
        try:
            assessment = Assessment.objects.get(pk=data.get('assessment', ''))
            assessment.score = assessment.compute_score(data)
            assessment.save()
            return HttpResponse('success')
        except Exception as e:
            print(e)
            return HttpResponse('success')
    assessment = Assessment.objects.create_assessment(quiz, request.GET.get('candidate-name', None))
    context = {'assessment': assessment}
    return render(request, 'main/assessment.html', context)

def add_question_choices(request, id):
    question = Question.objects.get(pk=id)
    ChoiceFormSet = modelformset_factory(Choice, extra=4, fields=['content'], max_num=4, validate_max=True)
    if request.method == 'POST':
        formset = ChoiceFormSet(request.POST, queryset=Choice.objects.none())
        if formset.is_valid():
            new_formset = formset.save(commit=False)
            for form in new_formset:
                form.question = question
                form.save()  
            return HttpResponseRedirect('/dashboard')
    else:
        formset = ChoiceFormSet(queryset=Choice.objects.none())
        context = {'formset': formset, 'question': question}
        return render(request, 'main/add_choices.html', context)


def edit_questions_choices(request, id):
    question = Question.objects.get(pk=id)
    ChoiceFormSet = modelformset_factory(Choice, extra=4, fields=['content'], max_num=4, validate_max=True)
    choices = question.choice_set.all()

    if request.method == 'POST':
        formset = ChoiceFormSet(request.POST, queryset=choices)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/dashboard')
    else:
        formset = ChoiceFormSet(queryset=choices)
        context = {'formset': formset, 'question': question}
        return render(request, 'main/edit_choices.html', context)


def create_quiz(request):
    QuestionFormSet = modelformset_factory(Question,extra=10, fields=['question', 'answer'],  max_num=10, validate_max=True)
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST)
        question_formset = QuestionFormSet(request.POST, queryset=Question.objects.none())
        if quiz_form.is_valid() and question_formset.is_valid():
            quiz_form.save()
            new_question_formset = question_formset.save(commit=False)

            for form in new_question_formset:             
                form.quiz = quiz_form.instance
                form.save() 
            return HttpResponseRedirect('/dashboard')
    else:
        quiz_form = QuizForm()
        question_formset = QuestionFormSet(queryset=Question.objects.none())
    context = {'quiz_form': quiz_form, 'question_formset': question_formset}
    return render(request, 'main/create_quiz.html', context)

def edit_quiz(request, id):
    quiz = Quiz.objects.get(pk=id)
    questions = quiz.question_set.all()
    QuestionFormSet = modelformset_factory(Question, fields=['question', 'answer'],  max_num=10, validate_max=True)
    if request.method == 'POST':
        quiz_form = QuizForm(request.POST, instance=quiz)
        question_formset = QuestionFormSet(request.POST, queryset=questions)
        if quiz_form.is_valid() and question_formset.is_valid():
            quiz_form.save()
            question_formset.save()
            return HttpResponseRedirect('/dashboard')
    else:
        quiz_form = QuizForm(instance=quiz)
        question_formset = QuestionFormSet(queryset=questions)
    context = {'quiz_form': quiz_form, 'question_formset': question_formset,'quiz': quiz}
    return render(request, 'main/edit_quiz.html', context)

def delete_quiz(request, id):
    quiz = Quiz.objects.get(pk=id)
    quiz.delete()
    return HttpResponseRedirect('/dashboard')
