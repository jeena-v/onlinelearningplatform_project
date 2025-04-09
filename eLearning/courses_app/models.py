from django.db import models
from accounts_app.models import CustomUser
import mimetypes

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'instructor'})
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='courses/images/', null=True, blank=True)


    def __str__(self):
        return self.title

class StudyMaterial(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='materials')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='study_materials/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    @property
    def file_type(self):
        mime_type, _ = mimetypes.guess_type(self.file.url)
        if mime_type:
            if mime_type.startswith('video'):
                return 'video'
            elif mime_type.startswith('image'):
                return 'image'
            elif mime_type == 'application/pdf':
                return 'pdf'
        return 'other'

    def __str__(self):
        return f"{self.title} - {self.course.title}"
    
from django.db import models
from django.contrib.auth import get_user_model

CustomUser = get_user_model()

class Enrollment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.course.title}"



