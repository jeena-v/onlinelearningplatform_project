from django.urls import path
from .import views

urlpatterns = [
        path('instructors_dashboard/',views.instructors_dashboard , name='instructors_dashboard'),
        path('course_details/<int:course_id>/',views.course_details , name='course_details'),
        path('<int:course_id>/view_materials/', views.view_materials, name='view_materials'),
        path('videos/', views.video_materials, name='video_materials'),
        path('pdfs/', views.pdf_materials, name='pdf_materials'),
        path("video/edit/<int:video_id>/", views.video_edit, name="video_edit"),
        path("video/delete/<int:video_id>/", views.video_delete, name="video_delete"),
        path("pdf/delete/<int:pdf_id>/", views.pdf_delete, name="pdf_delete"),
        path('instructors/students/', views.instructor_student_list, name='instructor_student_list'),  




]




