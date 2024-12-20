from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Content, Vote


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
        )

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long."
            )
        return value

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        return user


class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = (
            "title",
            "description",
        )


class VoteSerializer(serializers.ModelSerializer):
    content = serializers.PrimaryKeyRelatedField(
        queryset=Content.objects.all(),
    )

    class Meta:
        model = Vote
        fields = ["content", "score"]

    def validate_score(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Vote score must be between 0 and 5.")
        return value


class ContentDetailSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField()
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
    user_vote = serializers.SerializerMethodField()

    def get_user_vote(self, obj):
        user_id = self.context.get("user_id")
        if user_id is None:
            return None
        else:
            print("user_id", user_id)
            print("content_id", obj.id)
            vote = Vote.objects.filter(content_id=obj.id, user_id=user_id)
            if vote.exists():
                return vote.first().score
