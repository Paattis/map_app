from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from mapbackend.serializers.user import UserSerializer, UserRegistrationSerializer
from mapbackend.permissions import IsAdminOrUserItself
from rest_framework import generics


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = get_user_model().objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "put", "delete"]

    def get_queryset(self):
        if (self.request.user.is_superuser and self.request.user.is_staff):
            return super().get_queryset()

        # return only the logged in user if the user isn't an admin
        # mainly to discourage the harvesting of data through the API
        return super().get_queryset().filter(pk=self.request.user.id)


class RegisterView(generics.CreateAPIView):
    """Endpoint for the registration of a new user"""
    http_method_names = ["post"]

    queryset = get_user_model().objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
