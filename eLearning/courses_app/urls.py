from django.urls import path
from .import views

urlpatterns = [
    path('',views.index,name='index'),
    path('courses/',views.courses,name='courses'),
    path('course_list/', views.course_list, name='course_list'),
    path('create/', views.create_course, name='create_course'),
    path('<int:course_id>/',views.course_detail, name='course_detail'), 
    path('update/<int:pk>/', views.update_course, name='update_course'),
    path('delete/<int:pk>/', views.delete_course, name='delete_course'), 
    
    path('<int:course_id>/upload_material/', views.upload_material, name='upload_material'),
    path('<int:course_id>/enroll/', views.enroll_in_course, name='enroll_in_course'),
    path('my-courses/', views.enrolled_courses, name='enrolled_courses'),

    path('materials/<int:material_id>/edit/', views.edit_material, name='edit_material'),
    path('materials/<int:material_id>/delete/', views.delete_material, name='delete_material'),



]