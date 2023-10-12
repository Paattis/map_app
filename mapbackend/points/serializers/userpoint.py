from points.models import UserPoint
from rest_framework import serializers


class UserPointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserPoint
        fields = ['pk', 'label_text', 'position', 'user']
