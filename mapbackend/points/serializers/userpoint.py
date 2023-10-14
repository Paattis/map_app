from points.models import UserPoint
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from mapbackend.serializers import UserSerializerNoEmail
from rest_framework_gis.fields import GeometryField


class UserPointSerializer(serializers.ModelSerializer):
    """Simple model serializer for the UserPoint model."""
    user = UserSerializerNoEmail(read_only=True)

    class Meta:
        model = UserPoint
        fields = ["id", "label_text", "position", "user"]

    def create(self, validated_data):
        user = self.context["request"].user

        obj = self.Meta.model.objects.create(user=user, **validated_data)
        return obj
