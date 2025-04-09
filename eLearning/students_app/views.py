from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required

from courses_app.models import Course, Enrollment, StudyMaterial




@login_required
def students_dashboard(request):
    enrolled_courses = Enrollment.objects.filter(student=request.user)

    courses = Course.objects.all()  # You can filter by enrollment later if needed
    return render(request, 'students_app/students_dashboard.html', {'courses': courses,'enrolled_courses': enrolled_courses})

def my_course(request,course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = StudyMaterial.objects.filter(course=course)

    enrolled_courses = Enrollment.objects.filter(student=request.user)
    return render(request,'students_app/my_course.html', {'enrolled_courses': enrolled_courses,'course': course, 'materials': materials})

def profile_view(request):
    return render(request, 'students_app/profile.html')


from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import EditProfileForm  

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # after save, redirect to profile page
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'students_app/edit_profile.html', {'form': form})
