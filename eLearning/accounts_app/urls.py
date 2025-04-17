from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/student/', views.student_register, name='students_register'),
    path('register/instructor/', views.instructor_register, name='instructors_register'),
    path("login/", views.user_login, name="login"),
    path('logout/', views.user_logout, name='logout'),
   
    path('forgot-password/', views.custom_password_reset_view, name='forgot_password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts_app/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts_app/password_reset_complete.html'
    ), name='password_reset_complete'),

    
]
