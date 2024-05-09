from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        first_name,
        last_name,
        phone_number,
        password=None,
    ) -> "User":
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(
        self,
        email,
        password,
        first_name,
        last_name,
        phone_number,
    ) -> "User":
        if not email:
            raise ValueError("An email is required.")
        if not password:
            raise ValueError("A password is required.")
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
        )
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True

        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=150)
    last_name = models.CharField(_("last name"), max_length=150)
    email = models.EmailField(_("email address"), unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."))
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "first_name",
        "last_name",
        "phone_number",
    ]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"



class Vacancy(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    office = models.ForeignKey("Office", on_delete=models.CASCADE, related_name="vacancies")
    direction = models.ForeignKey("WorkDirection", on_delete=models.CASCADE, related_name="vacancies")
    
    def __str__(self):
        return self.title

class Office(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title
  
    
class WorkDirection(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Application(models.Model):
    resume = models.FileField(upload_to="applications")
    salary_expectations = models.CharField(max_length=32)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    accepted = models.BooleanField(null=True)
    def __str__(self):
        return f""