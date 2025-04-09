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

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from .forms import ForgotPasswordForm, ResetPasswordForm

User = get_user_model()

def forgot_password_view(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            request.session['reset_user'] = username_or_email
            return redirect('reset_password')
    else:
        form = ForgotPasswordForm()

    return render(request, 'accounts_app/forgot_password.html', {'form': form})

def reset_password_view(request):
    username_or_email = request.session.get('reset_user')

    if not username_or_email:
        return redirect('forgot_password')

    try:
        user = User.objects.get(username=username_or_email)
    except User.DoesNotExist:
        try:
            user = User.objects.get(email=username_or_email)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect('forgot_password')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.password = make_password(new_password)
            user.save()
            messages.success(request, "Password reset successfully! Please login.")
            return redirect('login')
    else:
        form = ResetPasswordForm()

    return render(request, 'accounts_app/reset_password.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout

