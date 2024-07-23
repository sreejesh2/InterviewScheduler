from rest_framework import serializers
from django.utils import timezone

from .models import Availability


class AvailabilitySerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])
    end_time = serializers.DateTimeField(input_formats=['%Y-%m-%d %H:%M'])

    class Meta:
        model = Availability
        fields = '__all__'

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        candidate = data.get('candidate')
        interviewer = data.get('interviewer')

        # Basic validation
        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        if start_time < timezone.now():
            raise serializers.ValidationError("Start time cannot be in the past.")

        if candidate and interviewer:
            raise serializers.ValidationError("Availability cannot be set for both candidate and interviewer simultaneously.")

        if not candidate and not interviewer:
            raise serializers.ValidationError("Availability must be set for either candidate or interviewer.")

        # Overlap check
        if self.check_overlap(start_time, end_time, candidate, interviewer):
            raise serializers.ValidationError("The new availability overlaps with an existing one.")

        return data

    def check_overlap(self, start_time, end_time, candidate, interviewer):
        # Determine if we are checking for a candidate or interviewer
        if candidate:
            existing_availabilities = Availability.objects.filter(
                candidate=candidate,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
        elif interviewer:
            existing_availabilities = Availability.objects.filter(
                interviewer=interviewer,
                start_time__lt=end_time,
                end_time__gt=start_time
            )
        else:
            return False

        # Debugging: Print the existing availabilities
        print(f"Checking overlap for {candidate or interviewer}:")
        for avail in existing_availabilities:
            print(f"Existing availability: {avail.start_time} to {avail.end_time}")

        # Return True if any overlapping availabilities are found
        return existing_availabilities.exists()