from typing import Any
from django.contrib.auth.forms import (
    BaseUserCreationForm,
    UserCreationForm,
    AuthenticationForm,
)
from django.contrib.auth import get_user_model
from django.forms import (
    CharField,
    ChoiceField,
    DateField,
    Field,
    ValidationError,
    ModelForm,
    Form,
)
from django import forms
from django.forms.widgets import DateInput
from .models import User, Application, Vacancy
from django.forms import widgets

User = get_user_model()


class SignupForm(BaseUserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "phone_number",
        )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError("User with this email already exists")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.phone_number = self.cleaned_data["phone_number"]
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm): ...

class ApplicationForm(ModelForm):
    full_name = forms.CharField(max_length=30, disabled=True)
    email = forms.EmailField(disabled=True)
    phone_number = forms.CharField(max_length=15, disabled=True)
    
    class Meta:
        model = Application
        fields = ["resume", "salary_expectations"]
    
    
    
    
    
    