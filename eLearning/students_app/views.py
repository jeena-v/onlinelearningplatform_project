from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from courses_app.forms import FeedbackForm
from django.db.models import Avg,Count
from courses_app.models import Assignment, Course, Enrollment, StudentSubmission, StudyMaterial,Feedback 

@login_required
def students_dashboard(request):
    enrolled_courses = Enrollment.objects.filter(student=request.user)

    # Annotate each course with average rating and student count
    courses = Course.objects.annotate(
        avg_rating=Avg('feedbacks__rating'),
        student_count=Count('enrollment')
    )

    return render(request, 'students_app/students_dashboard.html', {
        'courses': courses,
        'enrolled_courses': enrolled_courses
    })
@login_required   #enrolled students class and all study materials page
def my_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = StudyMaterial.objects.filter(course=course)
    assignments = Assignment.objects.filter(course=course)
    enrolled_courses = Enrollment.objects.filter(student=request.user)
    submissions = StudentSubmission.objects.filter(student=request.user)
    quizzes = course.quiz_set.all()  # Get quizzes for the course
    

    # Check enrollment
    if not Enrollment.objects.filter(student=request.user, course=course).exists():
        return redirect('students_dashboard')  # Block if not enrolled

    # Feedback logic
    feedbacks = course.feedbacks.all()
    average_rating = feedbacks.aggregate(Avg('rating'))['rating__avg']
    try:
        feedback_instance = Feedback.objects.get(course=course, user=request.user)
        form = FeedbackForm(instance=feedback_instance)
    except Feedback.DoesNotExist:
        feedback_instance = None
        form = FeedbackForm()

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback_instance)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.course = course
            feedback.user = request.user
            feedback.save()
            return redirect('my_course', course_id=course.id)

    return render(request, 'students_app/my_course.html', {
        'course': course,
        'materials': materials,
        'assignments': assignments,
        'enrolled_courses': enrolled_courses,
        'submissions': submissions,
        'feedbacks': feedbacks,
        'average_rating': average_rating,
        'form': form,
        'quizzes': quizzes,
    })


@login_required
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

@login_required
def assignments_page(request, course_id):
    # Retrieve the course using the course_id passed in the URL
    course = Course.objects.get(id=course_id)
    
    # Get the assignments for the specific course
    assignments = Assignment.objects.filter(course=course)
    
    # Get the submissions for the logged-in user
    submissions = StudentSubmission.objects.filter(student=request.user)
    submitted_assignment_ids = submissions.filter(student=request.user).values_list('assignment_id', flat=True)

    # Render the template and pass the course, assignments, and submissions
    return render(request, 'students_app/assignments_page.html', {
        'course': course,
        'assignments': assignments,
        'submissions': submissions,
        'submitted_assignment_ids': submitted_assignment_ids,
        'user': request.user
    })