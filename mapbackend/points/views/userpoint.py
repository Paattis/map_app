from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from points.serializers import UserPointSerializer
from points.models import UserPoint
from mapbackend.permissions import IsEditingOwnContent


class UserPointViewSet(viewsets.ModelViewSet):
    """
    Viewset that allows userpoints to be viewed, edited or deleted.

    list: Lists all the userpoints.

    retrieve: Gets the userpoint with the given id.

    update: Updates the userpoint with the given id. 
    Can only use this to update the userpoints of the currently logged in user if not staff or a superuser. 

    create: Creates a new userpoint.

    destroy: Deletes the userpoint with the given id.
    Can only use this to delete the userpoints of the currently logged in user if not staff or a superuser. 

    """

    queryset = UserPoint.objects.all().order_by("-created")
    serializer_class = UserPointSerializer
    permission_classes = [IsEditingOwnContent]
    http_method_names = ["get", "post", "put", "delete"]
