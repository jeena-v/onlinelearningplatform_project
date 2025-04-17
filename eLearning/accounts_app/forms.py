from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
from django.contrib.auth import get_user_model

class StudentRegisterForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    profile_picture = forms.ImageField(required=False)
    

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'bio','profile_picture']


class InstructorRegisterForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'bio', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'instructor'  # Ensuring user_type is set securely
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label="Username",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label="Password",
    )

# accounts_app/forms.py

from django import forms

class CustomPasswordResetForm(forms.Form):
    email = forms.EmailField(label='Enter your registered email')



