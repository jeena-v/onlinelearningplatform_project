from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Course, StudyMaterial
from .forms import CourseForm, StudyMaterialForm

def index(request):
    courses = Course.objects.all()
    return render(request, 'courses_app/index.html', {'courses': courses})



def courses(request):
    courses = Course.objects.all()
    studymaterials = StudyMaterial.objects.all()

    return render(request,'courses_app/courses.html',{'courses':courses,'studymaterials':studymaterials})


def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses_app/course_list.html', {'courses': courses})

@login_required
def create_course(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)   # <-- add request.FILES here
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = request.user
            course.save()
            return redirect('instructors_dashboard')
    else:
        form = CourseForm()
    return render(request, 'courses_app/create_course.html', {'form': form})


# Update Course
@login_required
def update_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)  # <-- add request.FILES
        if form.is_valid():
            form.save()
            return redirect('instructors_dashboard')
    else:
        form = CourseForm(instance=course)
    return render(request, 'instructors_app/update_course.html', {'form': form})


# Delete Course
@login_required
def delete_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == 'POST':
        course.delete()
        return redirect('instructors_dashboard')
    return render(request, 'instructors_app/course_delete.html', {'course': course})
    


@login_required
def upload_material(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    
    if request.user != course.instructor:
        return redirect('instructors_dashboard')

    if request.method == "POST":
        form = StudyMaterialForm(request.POST, request.FILES)  # form initialization
        if form.is_valid():
            material = form.save(commit=False)
            material.course = course
            material.save()
            return redirect('instructors_dashboard')
    else:
        form = StudyMaterialForm()  # form initialization for GET request
    
    return render(request, 'courses_app/upload_material.html', {'form': form, 'course': course})

from django.shortcuts import render, get_object_or_404
from .models import Course, StudyMaterial

def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = StudyMaterial.objects.filter(course=course)

    return render(request, 'courses_app/course_detail.html', {'course': course, 'materials': materials})


from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Course, Enrollment

@login_required
def enroll_in_course(request, course_id):
    course = Course.objects.get(id=course_id)
    
    # Prevent instructors from enrolling
    if request.user.user_type == "instructor":
        return HttpResponse("Instructors cannot enroll in courses.", status=403)

    # Create an enrollment record
    Enrollment.objects.get_or_create(student=request.user, course=course)

    return redirect('students_dashboard')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Enrollment

@login_required
def enrolled_courses(request):
    enrolled_courses = Enrollment.objects.filter(student=request.user)
    return render(request, 'courses_app/enrolled_courses.html', {'enrolled_courses': enrolled_courses})

@login_required
def edit_material(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    
    # Ensure only the instructor of the course can edit
    if request.user != material.course.instructor:
        return redirect('instructors_dashboard')

    if request.method == "POST":
        form = StudyMaterialForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return redirect('view_materials', course_id=material.course.id)
    else:
        form = StudyMaterialForm(instance=material)

    return render(request, 'courses_app/edit_material.html', {'form': form, 'material': material})


@login_required
def delete_material(request, material_id):
    material = get_object_or_404(StudyMaterial, id=material_id)
    
    # Ensure only the instructor of the course can delete
    if request.user != material.course.instructor:
        return redirect('instructors_dashboard')

    if request.method == "POST":
        course_id = material.course.id
        material.delete()
        return redirect('view_materials', course_id=course_id)

    return render(request, 'courses_app/delete_material.html', {'material': material})
