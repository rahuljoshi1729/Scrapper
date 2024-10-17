from rest_framework import serializers
from datetime import datetime


class userdataserializer(serializers.Serializer):
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    country = serializers.CharField()
    city = serializers.CharField()
    rating = serializers.IntegerField()
    maxRating = serializers.IntegerField()
    rank = serializers.CharField()
    maxRank = serializers.CharField()
    contribution = serializers.IntegerField()
    handle = serializers.CharField()
    friendOfCount = serializers.IntegerField()
    titlePhoto = serializers.CharField()
    avatar = serializers.CharField()
    organization = serializers.CharField()
    registrationTime = serializers.SerializerMethodField()
    lastOnlineTime = serializers.SerializerMethodField()
    
    def registrationTime(self, obj):
        return datetime.fromtimestamp(obj['registrationTimeSeconds']).strftime('%Y-%m-%d %H:%M:%S')

    def lastOnlineTime(self, obj):
        return datetime.fromtimestamp(obj['lastOnlineTimeSeconds']).strftime('%Y-%m-%d %H:%M:%S')

class submissionserializer(serializers.Serializer):
    contestId = serializers.IntegerField()
    creationTimeSeconds = serializers.CharField()
    

class ratingserializer(serializers.Serializer):
    contestId = serializers.IntegerField()
    contestName = serializers.CharField()
    handle = serializers.CharField()
    rank = serializers.IntegerField()
    oldRating = serializers.IntegerField()
    newRating = serializers.IntegerField()
    ratingUpdateTime = serializers.SerializerMethodField()
    
    def ratingUpdateTime(self, obj):
        return datetime.fromtimestamp(obj['ratingUpdateTimeSeconds']).strftime('%Y-%m-%d %H:%M:%S')