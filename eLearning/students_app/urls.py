from django.urls import path
from .import views

urlpatterns = [
       path('students_dashboard/',views.students_dashboard,name='students_dashboard'),
       path('my_course/<int:course_id>',views.my_course,name='my_course'),
       path('profile/',views.profile_view,name='profile'),
       path('profile/edit/', views.edit_profile, name='edit_profile'),




]
