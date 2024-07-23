from django.urls import path
from .views import RegisterAvailabilityView, SchedulableSlotsView

urlpatterns = [
    path('register-availability/', RegisterAvailabilityView.as_view(), name='register-availability'),
    path('schedulable-slots/<int:candidate_id>/<int:interviewer_id>/', SchedulableSlotsView.as_view(), name='schedulable-slots'),
]