from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from points.serializers import UserPointSerializer
from points.models import UserPoint
from mapbackend.permissions import IsEditingOwnContent


class UserPointViewSet(viewsets.ModelViewSet):
    """
    Viewset that allows userpoints to be viewed, edited or deleted.
    The texts below are to describe each of the HTTP methods 
    for the automatically generated documentation.
    (https://stackoverflow.com/a/58435631)

    list: Lists all the userpoints.

    retrieve: Gets the userpoint with the given id.

    update: Updates the userpoint with the given id. 
    Can only use this to update the userpoints of the currently logged in user if not staff or a superuser. 

    create: Creates a new userpoint. DRF's own OpenAPI generator has some trouble with
    some of the fields so the schema is represented wrong. The actual request body should actually be like the one below.
    ```
    {
        "label_text": "Foobar",
        "position": {
            "coordinates": [24.950, 60.17],
            "type": "Point",
        }
    }
    ```

    destroy: Deletes the userpoint with the given id.
    Can only use this to delete the userpoints of the currently logged in user if not staff or a superuser. 

    """

    queryset = UserPoint.objects.all().order_by("-created")
    serializer_class = UserPointSerializer
    permission_classes = [IsEditingOwnContent]
    http_method_names = ["get", "post", "put", "delete"]
