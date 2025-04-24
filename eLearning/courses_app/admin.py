from django.contrib import admin
from .models import ContactMessage, Course, Feedback, Question, Quiz, StudentSubmission,StudyMaterial,Enrollment ,Assignment

admin.site.register(Course)
admin.site.register(StudyMaterial)
admin.site.register(Enrollment)
admin .site.register(Assignment)
admin.site.register(ContactMessage)
admin.site.register(Quiz)
admin.site.register(Feedback)
admin.site.register(Question)
admin.site.register(StudentSubmission)




