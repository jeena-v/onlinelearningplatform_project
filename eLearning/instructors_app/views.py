from pyexpat.errors import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from courses_app.models import Course, Quiz, StudyMaterial, Enrollment


@login_required
def instructors_dashboard(request):
    courses = Course.objects.filter(instructor=request.user)
    # For each course, count the number of students enrolled
    quizzes = Quiz.objects.filter(instructor=request.user) 
    course_data = []
    for course in courses:
        student_count = Enrollment.objects.filter(course=course).count()
        course_data.append({
            'course': course,
            'student_count': student_count,
            'quizzes': quizzes
        })

    return render(request, 'instructors_app/instructors_dashboard.html', {
        'course_data': course_data
    })
        
@login_required
def instructor_student_list(request):
    # Get the instructor's courses
    courses = Course.objects.filter(instructor=request.user)

    # Fetch the students enrolled in those courses
    enrollments = Enrollment.objects.filter(course__in=courses)

    return render(request, 'instructors_app/student_list.html', {
        'enrollments': enrollments,
    })

@login_required
def view_materials(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Ensure only the instructor of the course can view materials
    if request.user != course.instructor:
        return redirect('instructors_dashboard')

    materials = StudyMaterial.objects.filter(course=course)
    return render(request, 'courses_app/view_materials.html', {'course': course, 'materials': materials})

@login_required
def video_materials(request):
    video_extensions = [".mp4", ".avi", ".mov", ".mkv"]
    
    # Get courses created by the logged-in instructor
    instructor_courses = Course.objects.filter(instructor=request.user)

    # Get videos uploaded under those courses
    videos = StudyMaterial.objects.filter(
        course__in=instructor_courses,  # Filter by instructor's courses
        file__iregex=r"\.(" + "|".join(ext.strip(".") for ext in video_extensions) + ")$"
    )

    return render(request, "instructors_app/video_list.html", {"videos": videos})

@login_required
def pdf_materials(request):
    instructor_courses = Course.objects.filter(instructor=request.user)  # Get instructor's courses
    pdfs = StudyMaterial.objects.filter(course__in=instructor_courses, file__iendswith=".pdf")
    
    return render(request, "instructors_app/pdf_list.html", {"pdfs": pdfs})

from django.shortcuts import render, get_object_or_404, redirect
from courses_app.models import StudyMaterial  # Ensure this model is correct
from courses_app.forms import StudyMaterialForm  # You need a form to edit the video

@login_required
def video_edit(request, video_id):
    video = get_object_or_404(StudyMaterial, id=video_id)
    
    if request.method == "POST":
        form = StudyMaterialForm(request.POST, request.FILES, instance=video)
        if form.is_valid():
            form.save()
            return redirect("video_materials")  # Redirect to video list after editing
    else:
        form = StudyMaterialForm(instance=video)

    return render(request, "instructors_app/video_edit.html", {"form": form})

@login_required
def video_delete(request, video_id):
    video = get_object_or_404(StudyMaterial, id=video_id)
    
    if request.method == "POST":
        course_id = video.course.id
        video.delete()
        return redirect('video_materials', course_id=course_id)
    return render(request, 'instructors_app/video_delete.html', {'video': video})

@login_required
def pdf_delete(request, pdf_id):
    pdf = get_object_or_404(StudyMaterial, id=pdf_id)
    
    if request.method == "POST":
        pdf.delete()
        messages.success(request, "PDF deleted successfully!")
        return redirect('pdf_materials')
    
    return render(request, 'instructors_app/pdf_delete.html', {'pdf': pdf})

from django.db.models import Avg
from courses_app.models import Feedback

def course_details(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    feedbacks = Feedback.objects.filter(course=course)
    average_rating = feedbacks.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0

    return render(request, "instructors_app/course_details.html", {
        "course": course,
        "feedbacks": feedbacks,
        "average_rating": average_rating,
    })



