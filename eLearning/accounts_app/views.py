from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .forms import StudentRegisterForm, InstructorRegisterForm, LoginForm
from django.contrib.auth import login as auth_login, authenticate
from django.contrib import messages

def student_register(request):
    if request.method == "POST":
        form = StudentRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('students_dashboard')  # Redirect to course page after login
    else:
        form = StudentRegisterForm()
    return render(request, 'accounts_app/students_register.html', {'form': form})

def instructor_register(request):
    if request.method == "POST":
        form = InstructorRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('instructors_dashboard')  # Redirect to instructor dashboard
    else:
        form = InstructorRegisterForm()
    return render(request, 'accounts_app/instructors_register.html', {'form': form})

def user_login(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            print(f"Attempting to authenticate user: {username}")
            print(f"Authentication result: {user}")

            if user is not None:
                print(f"Authenticated user: {user.username}, User Type: {user.user_type}")
                auth_login(request, user)

                if user.user_type == 'instructor':
                    print("Redirecting to instructor's dashboard.")
                    return redirect("instructors_dashboard")
                elif user.user_type == 'student':
                    print("Redirecting to student's dashboard.")
                    return redirect("students_dashboard")
                else:
                    print("Redirecting to the index page.")
                    return redirect("index")

            else:
                print("Invalid login attempt")  # Debugging
                messages.error(request, "Invalid username or password")
    if form.errors:
        messages.error(request, "There were some errors in your form.")

    return render(request, "accounts_app/login.html", {"form": form})

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import CustomPasswordResetForm
from django.conf import settings

User = get_user_model()  # Uses your custom user model

def custom_password_reset_view(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return render(request, 'accounts_app/password_reset_form.html', {
                    'form': form,
                    'error': 'No user is associated with this email.'
                })

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = request.build_absolute_uri(
            f'/accounts/reset/{uid}/{token}/'
            )


            subject = 'Reset Your Password'
            message = render_to_string('accounts_app/password_reset_email.html', {
                'user': user,
                'reset_link': reset_link
            })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            return render(request, 'accounts_app/password_reset_done.html')

    else:
        form = CustomPasswordResetForm()

    return render(request, 'accounts_app/password_reset_form.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

