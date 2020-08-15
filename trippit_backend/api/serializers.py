from django.contrib.auth.models import User
from .models import UserProfile
from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profilePicURL']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'profile']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user)
        return user

    def update(self, instance, validated_data):
        try:
            profile_data = validated_data.pop('profile')
        except:
            profile_data = None
            
        profile = instance.profile
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()
        profile.bio = profile_data.get('bio', profile.bio)
        profile.profilePicURL = profile_data.get('profilePicURL', profile.profilePicURL)
        profile.save()
        return instance