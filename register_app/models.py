from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import BaseUserManager
import uuid


# Create your models here.
GENDER_CHOICES = [
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("OTHER", "Other"),
]
USER_TYPE = [
    ("student", "Student"),
    ("teacher", "Teacher"),
    ("admin", "Admin"),
    ("driver", "Driver"),
    ("other", "Other"),
]
EMPLOYEE_TYPE = [
    ("part_time", "Part Time"),
    ("full_time", "Full Time"),
]

class DateTimeMixin(models.Model): # you can use this field in every modal class model_name(datetimemixin) 
    id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        primary_key=True,
        auto_created=True,
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True  # this will allow you to inherit this in another 

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class User(AbstractUser, DateTimeMixin):
    email = models.EmailField(
        unique=True,
        verbose_name=_("Email ID"),
        blank=True,
        null=True,
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    gender = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        choices=GENDER_CHOICES,
        verbose_name=_("Gender"),
    )
    date_of_birth = models.DateField(_("Date of Birth"), null=True, blank=True)
    address = models.CharField(_("Address"), max_length=255, null=True, blank=True)
    zip_code = models.CharField(_("ZIP Code"), max_length=10, null=True, blank=True)
    bio = models.TextField(_("Bio"), null=True, blank=True)
    user_type = models.CharField(
        max_length=8,
        blank=True,
        null=True,
        choices=USER_TYPE,
        verbose_name=_("User Type"),
    )
    employee_type = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        choices=EMPLOYEE_TYPE,
        verbose_name=_("Employee Type"),
    )
    # position = models.ForeignKey(
    #     EmployeePosition,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    #     verbose_name=_("Position"),
    # )
    # class_name = models.ForeignKey(
    #     ClassDetails,
    #     on_delete=models.CASCADE,
    #     blank=True,
    #     null=True,
    #     verbose_name=_("Class"),
    # )
    photo = models.FileField(upload_to="media/student/profile/", null=True, blank=True)
    mother_first_name = models.CharField(max_length=100, null=True, blank=True)
    mother_middle_name = models.CharField(max_length=100, null=True, blank=True)
    mother_last_name = models.CharField(max_length=100, null=True, blank=True)
    father_first_name = models.CharField(max_length=100, null=True, blank=True)
    father_middle_name = models.CharField(max_length=100, null=True, blank=True)
    father_last_name = models.CharField(max_length=100, null=True, blank=True)
    mother_contact_no = models.CharField(max_length=50, null=True, blank=True)
    father_contact_no = models.CharField(max_length=50, null=True, blank=True)

    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

    # @property
    # def fullname(self):
    #     return self.get_full_name()


class OTP(DateTimeMixin):
    email=models.EmailField()
    otp=models.CharField(max_length=4)
    token=models.CharField(max_length=12,blank=True,null=True)

    def __str__(self):
            return f"{self.email} - {self.otp}"