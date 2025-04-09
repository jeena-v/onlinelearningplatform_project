from django.contrib import admin
from .models import Course,StudyMaterial,Enrollment

admin.site.register(Course)
admin.site.register(StudyMaterial)
admin.site.register(Enrollment)

