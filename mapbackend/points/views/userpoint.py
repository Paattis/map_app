from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from points.serializers import UserPointSerializer
from points.models import UserPoint


class UserPointViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = UserPoint.objects.all().order_by('-created')
    serializer_class = UserPointSerializer
    permission_classes = [permissions.AllowAny]
