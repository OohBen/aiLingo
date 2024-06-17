from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    profile_pic = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "name",
            "profile_pic",
            "date_joined",
            "is_premium",
            "home_language",
        ]

    def get_profile_pic(self, obj):
        if obj.profile_pic:
            return self.context.get('request').build_absolute_uri(obj.profile_pic.url)
        return None


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
            model = User
            fields = [
                "id",
                "email",
                "name",
                "profile_pic",
                "date_joined",
                "is_premium",
                "password",
                "home_language",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        home_language_id = validated_data.pop("home_language", None)
        user = User.objects.create(**validated_data)
        user.set_password(password)
        if home_language_id:
            user.home_language_id = home_language_id
        user.save()
        return user
