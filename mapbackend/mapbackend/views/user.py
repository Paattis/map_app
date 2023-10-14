from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from mapbackend.serializers.user import UserSerializer
from mapbackend.permissions import IsAdminOrUserItself


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if (self.request.user.is_superuser and self.request.user.is_staff):
            return super().get_queryset()

        # return only the logged in user if the user isn't an admin
        return super().get_queryset().filter(pk=self.request.user.id)
