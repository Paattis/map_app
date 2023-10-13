from points.models import UserPoint
from rest_framework import serializers
from rest_framework.exceptions import ParseError

class UserPointSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserPoint
        fields = ['pk', 'label_text', 'position', 'user_id']

    def create(self, validated_data):
        user = self.context["request"].user

        obj = self.Meta.model.objects.create(user=user,**validated_data)
        return obj
