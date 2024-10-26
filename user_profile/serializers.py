from rest_framework import serializers

from user_profile.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'name', 'physical_appearance', 'interests', 'age', 'nature']
        read_only_fields = ['user']
    
    def validate_age(self, value):
        if value < 0:
            raise serializers.ValidationError("Age cannot be negative")
        return value

class LoginResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    profile = UserProfileSerializer(required=False)