from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions
from mapbackend.serializers.user import UserSerializer, UserRegistrationSerializer
from mapbackend.permissions import IsAdminOrUserItself
from rest_framework import generics


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited. 
    The texts below are to describe each of the HTTP methods 
    for the automatically generated documentation.
    (https://stackoverflow.com/a/58435631)

    list: Lists users. If not logged in as a staff 
    or a superuser this only returns the currently logged in user.

    retrieve: Gets the user with the given id. Can only use this to access the currently logged in user 
    if not staff or a superuser.

    update: Updates the user with the given id. Can only use this to access the currently logged in user 
    if not staff or a superuser.
    destroy: Deletes the user with the given id. Can only use this to delete the currently logged in user 
    if not staff or a superuser.
    """

    queryset = get_user_model().objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "put", "delete"]

    def get_queryset(self):
        if self.request.user.is_superuser and self.request.user.is_staff:
            return super().get_queryset()

        # return only the logged in user if the user isn't an admin
        # mainly to discourage the harvesting of data through the API
        return super().get_queryset().filter(pk=self.request.user.id)


class RegisterView(generics.CreateAPIView):
    """Endpoint for the registering a new user. 
    `username` and `email` must be unique."""

    http_method_names = ["post"]

    queryset = get_user_model().objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegistrationSerializer
