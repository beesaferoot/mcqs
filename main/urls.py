from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('story', views.story),
    path('dashboard', views.dashboard),
    path('dashboard/edit_quiz/<int:id>/', views.edit_quiz),
    path('dashboard/create_quiz', views.create_quiz),
    path('dashboard/add_question_choices/<int:id>/', views.add_question_choices),
    path('dashboard/edit_question_choices/<int:id/', views.edit_questions_choices),
    path('assessment/instruction/quiz/<int:id>/', views.assessment_instruction),
    path('assessment/quiz/<int:id>/', views.assessment_quiz),
    path('assessments/results', views.assessment_results)
]