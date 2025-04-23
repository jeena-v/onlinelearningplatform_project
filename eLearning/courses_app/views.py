from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from accounts_app.models import CustomUser
from .models import Assignment, Course, Feedback, StudyMaterial,Enrollment,ContactMessage,StudentSubmission
from .forms import AssignmentForm, CourseForm, FeedbackForm, QuizForm, StudyMaterialForm, ContactForm, StudentSubmissionForm
from django.db.models import Q
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings


def about(request):
    return render(request,'courses_app/about.html')

def contact(request):
    return render(request,'courses_app/contact.html')

def index(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'student':
            return redirect('students_dashboard')
        elif request.user.user_type == 'instructor':
            return redirect('instructors_dashboard')

    courses = Course.objects.all()

    for course in courses:
        course.student_count = course.enrollment_set.count()
        course.average_rating = course.feedbacks.aggregate(avg=Avg('rating'))['avg'] or 0

    instructors = CustomUser.objects.filter(user_type='instructor')

    return render(request, 'courses_app/index.html', {
        'courses': courses,
        'instructors': instructors
    })


def instructor_detail(request, instructor_id):
    # Get the instructor by their ID (ensuring they are an instructor)
    instructor = get_object_or_404(CustomUser, id=instructor_id, user_type='instructor')
    
    # Get all courses taught by this instructor
    courses = Course.objects.filter(instructor=instructor)
    
    # Pass the instructor and their courses to the template
    return render(request, 'courses_app/instructor_detail.html', {'instructor': instructor, 'courses': courses})

def courses(request):
    query = request.GET.get('q')
    instructor = request.GET.get('instructor')

    courses = Course.objects.all()

    if query:
        courses = courses.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        )

    if instructor:
        courses = courses.filter(
            instructor__username__icontains=instructor
        )

    course_data = []
    for course in courses:
        student_count = Enrollment.objects.filter(course=course).count()
        average_rating = course.feedbacks.aggregate(avg=Avg('rating'))['avg'] or 0

        course_data.append({
            'course': course,
            'student_count': student_count,
            'average_rating': average_rating  
        })

    return render(request, 'courses_app/courses.html', {
        'course_data': course_data
    })



def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses_app/course_list.html', {'courses': courses})

@login_required
def create_course(request):                             #create course
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)   
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
        form = CourseForm(request.POST, request.FILES, instance=course)  
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

#upload/add studymaterials    
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

#course details
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    materials = StudyMaterial.objects.filter(course=course)

    return render(request, 'courses_app/course_detail.html', {'course': course, 'materials': materials})

@login_required
def enroll_in_course(request, course_id):
    course = Course.objects.get(id=course_id)
    
    # Prevent instructors from enrolling
    if request.user.user_type == "instructor":
        return HttpResponse("Instructors cannot enroll in courses.", status=403)

    # Create an enrollment record
    Enrollment.objects.get_or_create(student=request.user, course=course)

    return redirect('students_dashboard')

#enrolled courses
@login_required
def enrolled_courses(request):
    enrolled_courses = Enrollment.objects.filter(student=request.user)
    return render(request, 'courses_app/enrolled_courses.html', {'enrolled_courses': enrolled_courses})

#edit studymaterials
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

#create assignment
@login_required
def add_assignment(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST, user=request.user)  
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.instructor = request.user
            assignment.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm(user=request.user)  
    return render(request, "courses_app/assignment_form.html", {"form": form})

#assignment list
@login_required
def assignment_list(request):
    assignments = Assignment.objects.filter(instructor=request.user)
    return render(request, "courses_app/assignment_list.html", {"assignments": assignments})

@login_required
def edit_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)

    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment, user=request.user)  # pass user
        if form.is_valid():
            form.save()
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment, user=request.user)  # pass user

    return render(request, "courses_app/assignment_edit.html", {"form": form})

@login_required                      #delete assignment
def delete_assignment(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == "POST":
        assignment.delete()
        return redirect('assignment_list')
    return render(request, "courses_app/assignment_delete.html", {"assignment": assignment})

@login_required                      #assignment submission
def submit_assignment(request, assignment_id):
    assignment = Assignment.objects.get(id=assignment_id)

    if request.method == 'POST':
        form = StudentSubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.student = request.user
            submission.assignment = assignment
            submission.save()
            return redirect('students_dashboard')  # Redirect after successful submission
    else:
        form = StudentSubmissionForm()

    return render(request, 'students_app/submit_assignment.html', {'form': form, 'assignment': assignment})

@login_required
def view_submissions(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    submissions = StudentSubmission.objects.filter(assignment=assignment)

    # Optional: Check that there are submissions for the assignment
    if not submissions:
        submissions = None

    return render(request, 'courses_app/view_submissions.html', {'assignment': assignment, 'submissions': submissions})

@login_required               #assignment evaluation
def evaluate_submission(request, submission_id):
    submission = StudentSubmission.objects.get(id=submission_id)

    if request.method == 'POST':
        feedback = request.POST.get('feedback')
        grade = request.POST.get('grade')
        submission.feedback = feedback
        submission.grade = grade
        submission.save()
        return redirect('view_submissions', assignment_id=submission.assignment.id)

    return render(request, 'courses_app/evaluate_submission.html', {'submission': submission})

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to DB
            contact = ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )

            # Send Email
            send_mail(
                subject=f"New Contact Message: {contact.subject}",
                message=f"Name: {contact.name}\nEmail: {contact.email}\n\nMessage:\n{contact.message}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=['your_email@gmail.com'],  #  receive messages
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent and saved successfully!')
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'courses_app/contact.html', {'form': form})

@login_required
def submit_feedback(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    # Check if user is enrolled
    if not Enrollment.objects.filter(user=request.user, course=course).exists():
        return render(request, 'courses_app/not_enrolled.html')

    feedback_instance = Feedback.objects.filter(user=request.user, course=course).first()

    if request.method == 'POST':
        form = FeedbackForm(request.POST, instance=feedback_instance)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.course = course
            feedback.save()
            return redirect('course_details', course_id=course.id)
    else:
        form = FeedbackForm(instance=feedback_instance)

    return render(request, 'courses_app/submit_feedback.html', {'form': form, 'course': course})
#quiz creation
@login_required
def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST, user=request.user)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.instructor = request.user
            quiz.save()
            return redirect('add_question', quiz_id=quiz.id)
    else:
        form = QuizForm(user=request.user)

    return render(request, 'courses_app/create_quiz.html', {'form': form})


from .models import Quiz, Question
from .forms import QuestionForm

@login_required                          #add questions for created quiz
def add_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)  # Get the quiz object by quiz_id
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz  # Associate the question with the selected quiz
            question.save()
            return redirect('add_question', quiz_id=quiz.id)  # Redirect back to add more questions
    else:
        form = QuestionForm()

    return render(request, 'courses_app/add_question.html', {'form': form, 'quiz': quiz})

@login_required            #quiz list
def quiz_list(request):
    quizzes = Quiz.objects.filter(instructor=request.user)
    return render(request, 'courses_app/quiz_list.html', {'quizzes': quizzes})

#student attend quiz
@login_required                  
def student_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        score = 0
        total = questions.count()

        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            print(f"Q: {question.text} | Selected: {selected} | Correct: {question.correct_option}")

            if selected and selected.upper() == question.correct_option.upper():
                score += 1

        percentage = round((score / total) * 100, 2)

        # Redirect to result page with score data 
        return render(request, 'courses_app/quiz_result.html', {
            'quiz': quiz,
            'score': score,
            'total': total,
            'percentage': percentage,
        })

    return render(request, 'courses_app/attempt_quiz.html', {
        'quiz': quiz,
        'questions': questions,
    })

@login_required                 #edit quiz
def edit_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, instructor=request.user)
    if request.method == 'POST':
        form = QuizForm(request.POST, instance=quiz)
        if form.is_valid():
            form.save()
            return redirect('quiz_list')
    else:
        form = QuizForm(instance=quiz)
    return render(request, 'courses_app/edit_quiz.html', {'form': form})


@login_required       #delete quiz
def delete_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id, instructor=request.user)
    if request.method == "POST":
        quiz.delete()
        return redirect('quiz_list')
    return render(request, "courses_app/delete_quiz.html", {"quiz": quiz})