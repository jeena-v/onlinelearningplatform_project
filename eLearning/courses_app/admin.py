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

# admin.py
from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'amount', 'status', 'order_id', 'payment_id', 'created_at')
    search_fields = ('user__username', 'course__title', 'order_id', 'payment_id')
    list_filter = ('status', 'created_at')



