from django.contrib import admin
from .models import*


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    model = Choice

    def save_model(self, request, obj, form, change):
        if change:
            super().save_model(request, obj, form, change)
        else:
            try:
                obj.question.add_option(obj)
            except Exception as e:
                print(e)


class ChoiceInline(admin.StackedInline):
    model = Choice



@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    model = Question
    inlines = [ChoiceInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    model = Quiz


@admin.register(Assessment)
class AdminAssessment(admin.ModelAdmin):
    model = Assessment