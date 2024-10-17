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

    def get_registrationTime(self, obj):
        # Convert registrationTimeSeconds to a readable timestamp
        return datetime.fromtimestamp(obj['registrationTimeSeconds']).strftime('%Y-%m-%d %H:%M:%S')

    def get_lastOnlineTime(self, obj):
        # Convert lastOnlineTimeSeconds to a readable timestamp
        return datetime.fromtimestamp(obj['lastOnlineTimeSeconds']).strftime('%Y-%m-%d %H:%M:%S')   