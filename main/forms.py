from django import forms
from .models import Quiz, Question, Choice

class QuizForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Quiz
        fields = ['title', 'time_frame', 'description' ]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['quiz', 'question', 'answer']

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['question', 'content']