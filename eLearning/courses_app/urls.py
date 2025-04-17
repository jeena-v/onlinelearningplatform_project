from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('courses/',views.courses,name='courses'),
    path('about',views.about,name='about'),
    path('contact',views.contact,name='contact'),
    path('contact/',views.contact_view, name='contact'),


    path('instructor/<int:instructor_id>/', views.instructor_detail, name='instructor_detail'),

    path('course_list/', views.course_list, name='course_list'),
    path('create/', views.create_course, name='create_course'),
    path('<int:course_id>/',views.course_detail, name='course_detail'), 
    path('update/<int:pk>/', views.update_course, name='update_course'),
    path('delete/<int:pk>/', views.delete_course, name='delete_course'), 
    
    path('<int:course_id>/upload_material/', views.upload_material, name='upload_material'),
    path('materials/<int:material_id>/edit/', views.edit_material, name='edit_material'),
    path('materials/<int:material_id>/delete/', views.delete_material, name='delete_material'),

    path('my-courses/', views.enrolled_courses, name='enrolled_courses'),
    path('<int:course_id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
   
    path("assignments/", views.assignment_list, name="assignment_list"),
    path("assignments/add/", views.add_assignment, name="add_assignment"),
    path("assignments/<int:pk>/edit/", views.edit_assignment, name="edit_assignment"),
    path("assignments/<int:pk>/delete/", views.delete_assignment, name="delete_assignment"),
    path('submit-assignment/<int:assignment_id>/', views.submit_assignment, name='submit_assignment'),
    path('assignment/<int:assignment_id>/submissions/', views.view_submissions, name='view_submissions'),
    path('submission/<int:submission_id>/evaluate/', views.evaluate_submission, name='evaluate_submission'),
    path('submit/<int:course_id>/', views.submit_feedback, name='submit_feedback'),

    path('create-quiz/', views.create_quiz, name='create_quiz'),
    path('quiz/<int:quiz_id>/', views.student_quiz, name='student_quiz'),
    path('quiz/<int:quiz_id>/attempt/', views.student_quiz, name='student_quiz'),

    path('quiz/<int:quiz_id>/add-question/', views.add_question, name='add_question'),
    path('quizzes/', views.quiz_list, name='quiz_list'),
    path('quiz/<int:quiz_id>/edit/', views.edit_quiz, name='edit_quiz'),
    path('quiz/<int:quiz_id>/delete/', views.delete_quiz, name='delete_quiz'),


]






