from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from datetime import timedelta

from InterviewScheduler.settings import SCHEDULER_HOUR_DURATION
from utils import logger
from accounts.models import Interviewer, Candidate
from .models import Availability
from .serializers import AvailabilitySerializer
from .utils import convert_to_readable_format

logger = logger.get_logger("SchedulerView")

class RegisterAvailabilityView(generics.CreateAPIView):
    """
    API view to register availability for an interviewer or candidate.
    """
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create new availability records.
        """
        serializer = self.get_serializer(data=request.data)
        logger.info(f"Received availability registration request: {request.data}")

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            logger.info("Availability registered successfully.")

            response_data = {
                "status": 1,
                "message": "Availability registered successfully.",
                "data": serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            logger.error(f"Error occurred while registering availability: {str(e)}")
            response_data = {
                "status": 0,
                "message": f"Error occurred while registering availability: {str(e)}"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)



class SchedulableSlotsView(APIView):
    """
    API view to retrieve common schedulable slots for a candidate and an interviewer.
    """
    def get(self, request, candidate_id, interviewer_id):
        """
        Handles GET requests to find common available slots between a candidate and an interviewer.
        """
        try:
            candidate = get_object_or_404(Candidate, id=candidate_id)
            interviewer = get_object_or_404(Interviewer, id=interviewer_id)
            logger.info(f"Retrieving availabilities for candidate {candidate_id} and interviewer {interviewer_id}")
            
            candidate_availabilities = Availability.objects.filter(candidate=candidate).order_by('start_time')
            interviewer_availabilities = Availability.objects.filter(interviewer=interviewer).order_by('start_time')
            
            slots = []
            i, j = 0, 0
            
            while i < len(candidate_availabilities) and j < len(interviewer_availabilities):
                c_avail = candidate_availabilities[i]
                i_avail = interviewer_availabilities[j]
                
                start = max(c_avail.start_time, i_avail.start_time)
                end = min(c_avail.end_time, i_avail.end_time)
                
                while start + timedelta(hours=SCHEDULER_HOUR_DURATION) <= end:
                    slots.append((start, start + timedelta(hours=SCHEDULER_HOUR_DURATION)))
                    start += timedelta(hours=SCHEDULER_HOUR_DURATION)
                
                if c_avail.end_time < i_avail.end_time:
                    i += 1
                else:
                    j += 1

            if not slots:
                logger.info("No common available slots found.")
                return Response(
                    {"status": 0, "message": "No common available slots found."}, 
                    status=status.HTTP_404_NOT_FOUND
                )

            readable_slots = convert_to_readable_format([(s.isoformat(), e.isoformat()) for s, e in slots])
            logger.info("Common available slots found and retrieved successfully.")
            
            return Response(
                {"status": 1, "data": readable_slots, "message": "Slots retrieved successfully."}, 
                status=status.HTTP_200_OK
            )
        
        except Exception as e:
            logger.error(f"An error occurred while retrieving schedulable slots: {str(e)}")
            return Response(
                {"status": 0, "error": f"An error occurred: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        