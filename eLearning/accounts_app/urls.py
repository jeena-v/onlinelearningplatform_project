from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/student/', views.student_register, name='students_register'),
    path('register/instructor/', views.instructor_register, name='instructors_register'),
    path("login/", views.user_login, name="login"),
    path('logout/', views.user_logout, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/', views.reset_password_view, name='reset_password'),

    
]
