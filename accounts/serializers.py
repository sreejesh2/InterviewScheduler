from rest_framework import serializers

from .models import Interviewer,Candidate


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'

class InterviewerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interviewer
        fields = '__all__'
