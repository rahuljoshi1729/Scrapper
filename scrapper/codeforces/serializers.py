from rest_framework import serializers
from datetime import datetime

class userdataserializer(serializers.Serializer):
    firstName = serializers.CharField(source='firstName')
    lastName = serializers.CharField(source='lastName')
    country = serializers.CharField(source='country')
    city = serializers.CharField(source='city')
    rating = serializers.IntegerField(source='rating')
    maxRating = serializers.IntegerField(source='maxRating')
    rank = serializers.CharField(source='rank')
    maxRank = serializers.CharField(source='maxRank')
    contribution = serializers.IntegerField(source='contribution')
    handle = serializers.CharField(source='handle')
    friendOfCount = serializers.IntegerField(source='friendOfCount')
    titlePhoto = serializers.CharField(source='titlePhoto')
    avatar = serializers.CharField(source='avatar')
    organization = serializers.CharField(source='organization')
    registrationTime = serializers.SerializerMethodField(source='registrationTimeSeconds', format='%Y-%m-%d %H:%M:%S')
    lastOnlineTime = serializers.SerializerMethodField(source='lastOnlineTimeSeconds',format='%Y-%m-%d %H:%M:%S')

class submissionserializer(serializers.Serializer):
    contest_id = serializers.IntegerField(source='contestId')
    creation_time = serializers.DateTimeField(source='creationTimeSeconds', format='%Y-%m-%d %H:%M:%S')

class ratingserializer(serializers.Serializer):
    contestId = serializers.IntegerField(source='contestId')
    contestName = serializers.CharField(source='contestName')
    handle = serializers.CharField(source='handle')
    rank = serializers.IntegerField(source='rank')
    oldRating = serializers.IntegerField(source='oldRating')
    newRating = serializers.IntegerField(source='newRating')
    ratingUpdateTime = serializers.SerializerMethodField(source='ratingUpdateTimeSeconds',format='%Y-%m-%d %H:%M:%S')