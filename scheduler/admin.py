from django.contrib import admin
from .models import Interviewer,Candidate,Availability
# Register your models here.
admin.site.register(Interviewer)
admin.site.register(Candidate)
admin.site.register(Availability)