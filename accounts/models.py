from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.


class Candidate(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True,blank=True)
    phone_number = models.CharField(max_length=15, unique=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if not self.phone_number.isdigit():
            raise ValidationError("Phone number must contain only digits.")

class Interviewer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, unique=True)
    specialization = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name

    def clean(self):
        if not self.phone_number.isdigit():
            raise ValidationError("Phone number must contain only digits.")