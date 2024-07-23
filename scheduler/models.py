from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import Interviewer, Candidate


class Availability(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True, blank=True)
    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE, null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.candidate or self.interviewer} available from {self.start_time} to {self.end_time}"
    


