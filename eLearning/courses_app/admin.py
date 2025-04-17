from django.contrib import admin
from .models import ContactMessage, Course,StudyMaterial,Enrollment ,Assignment

admin.site.register(Course)
admin.site.register(StudyMaterial)
admin.site.register(Enrollment)
admin .site.register(Assignment)
admin.site.register(ContactMessage)
