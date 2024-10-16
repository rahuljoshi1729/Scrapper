from rest_framework import serializers

#user user data serializer
class userdataserializer(serializers.Serializer):
    realName = serializers.CharField(required=False, allow_blank=True)
    userAvatar = serializers.URLField(required=False, allow_blank=True)
    birthday = serializers.CharField(required=False, allow_blank=True)
    ranking = serializers.IntegerField(required=False, allow_null=True)
    reputation = serializers.IntegerField(required=False, allow_null=True)
    websites = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    countryName = serializers.CharField(required=False, allow_blank=True)
    company = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    school = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    skillTags = serializers.ListField(child=serializers.CharField(), required=False, allow_empty=True)
    aboutMe = serializers.CharField(required=False, allow_blank=True)
    starRating = serializers.FloatField(required=False, allow_null=True)

    # Contributions data
    points = serializers.IntegerField(required=False)
    questionCount = serializers.IntegerField(required=False)
    testcaseCount = serializers.IntegerField(required=False)

    # Badge data
    badges = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField(), required=False),
        required=False, allow_empty=True
    )
    upcomingBadges = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField(), required=False),
        required=False, allow_empty=True
    )
    activeBadge = serializers.DictField(child=serializers.CharField(), required=False, allow_null=True)

    # Submission stats
    totalSubmissionNum = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField(), required=False),
        required=False, allow_empty=True
    )
    acSubmissionNum = serializers.ListField(
        child=serializers.DictField(child=serializers.IntegerField(), required=False),
        required=False, allow_empty=True
    )

    # Submission calendar data
    submissionCalendar = serializers.JSONField(required=False)

    # User details
    username = serializers.CharField()
    githubUrl = serializers.URLField(required=False, allow_null=True)
    twitterUrl = serializers.URLField(required=False, allow_null=True)
    linkedinUrl = serializers.URLField(required=False, allow_null=True)

    # All questions count
    allQuestionsCount = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField(), required=False),
        required=False, allow_empty=True
    )

    # Recent submissions
    recentSubmissionList = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField(), required=False),
        required=False, allow_empty=True
    )

    # Contributions nested object
    contributions = serializers.DictField(child=serializers.IntegerField(), required=False)

    # Contest details
    attendedContestsCount = serializers.IntegerField(required=False, allow_null=True)
    rating = serializers.FloatField(required=False, allow_null=True)
    globalRanking = serializers.IntegerField(required=False, allow_null=True)
    totalParticipants = serializers.IntegerField(required=False, allow_null=True)
    topPercentage = serializers.FloatField(required=False, allow_null=True)
    badge = serializers.CharField(required=False, allow_blank=True)
    contestHistory = serializers.ListField(
        child=serializers.DictField(child=serializers.CharField(), required=False),
        required=False, allow_empty=True
    )