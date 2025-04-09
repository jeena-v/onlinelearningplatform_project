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




User = get_user_model()

class ForgotPasswordForm(forms.Form):
    username_or_email = forms.CharField(max_length=255, label="Username or Email")

    def clean_username_or_email(self):
        data = self.cleaned_data['username_or_email']
        if not User.objects.filter(username=data).exists() and not User.objects.filter(email=data).exists():
            raise forms.ValidationError("User not found.")
        return data

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")

        return cleaned_data
