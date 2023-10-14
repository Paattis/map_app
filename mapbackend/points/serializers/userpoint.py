from points.models import UserPoint
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from mapbackend.serializers import UserSerializer


class UserPointSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserPoint
        fields = ['pk', 'label_text', 'position', 'user']

    def create(self, validated_data):
        user = self.context["request"].user

        obj = self.Meta.model.objects.create(user=user, **validated_data)
        return obj
