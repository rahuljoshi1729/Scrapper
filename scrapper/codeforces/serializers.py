from rest_framework import serializers
from datetime import datetime

class submissionserializer(serializers.Serializer):
    contestId = serializers.IntegerField()
    creationTimeSeconds = serializers.CharField()
    

