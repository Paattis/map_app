from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    """Simple serializer for users."""

    class Meta:
        model = get_user_model()
        fields = ["id", "username", "email"]


class UserSerializerNoEmail(serializers.ModelSerializer):
    """User serializer with less information available to discourage data scraping.
    Used for displaying the user's id and name in the Userpoints they've created."""

    class Meta:
        model = get_user_model()
        fields = ["id", "username"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""

    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())],
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = get_user_model()
        fields = ["username", "email", "password", "password2", "id"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError("Passwords need to match!")

        return attrs

    def create(self, validated_data: dict):
        user = self.Meta.model.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user
