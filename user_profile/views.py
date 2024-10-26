import logging
from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotFound
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import viewsets, permissions


from user_profile.models import UserProfile
from user_profile.serializers import LoginResponseSerializer, UserProfileSerializer

class PasswordLessLoginView(APIView):

    def post(self, request, username):
        user = get_user_model().objects.get_or_create(username=username)
        user = user[0]

        profile = None
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            logging.info("New User Added")
        
        token = AccessToken.for_user(user)

        response = {
            'token': str(token)
        }

        if profile:
            response['profile'] = model_to_dict(profile)
        serial = LoginResponseSerializer(data=response)

        serial.is_valid(raise_exception=True)

        return Response(serial.validated_data)
    
class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own profile unless they're staff
        if self.request.user.is_staff:
            return UserProfile.objects.all()
        try:
            return UserProfile.objects.filter(user=self.request.user)
        except UserProfile.DoesNotExist:
            raise NotFound("Profile not found")
    
    def perform_create(self, serializer):
        # Check if user already has a profile
        try:
            UserProfile.objects.get(user=self.request.user)
            raise PermissionDenied("User profile already exists")
        except UserProfile.DoesNotExist:
            serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        # Users can only update their own profile unless they're staff
        profile = self.get_object()
        if profile.user != self.request.user and not self.request.user.is_staff:
            raise PermissionDenied("You don't have permission to edit this profile")
        serializer.save()
