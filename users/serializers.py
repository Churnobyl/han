from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
import random, string

from users.models import User, Achievement
from users.customtoken import user_email_verify_token
from users.models import User
from django.contrib.sessions.models import Session


def password_maker():
    """임시 비밀번호 생성기

    Returns:
        new password : 랜덤으로 영문+숫자 6개 조합의 문자열을 뱉음
    """
    random_str = string.ascii_letters + string.digits
    return "".join(random.choice(random_str) for _ in range(6))


class PasswordResetSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email",)

    def update(self, instance, validated_data):
        password = password_maker()
        instance.set_password(password)
        instance.save()

        to_email = instance.email
        email = EmailMessage(
            "<한> 계정 비밀번호 초기화",
            f"변경 된 임시 비밀번호는 {password}입니다. \n\n로그인 후 반드시 회원정보에서 비밀번호를 변경해주세요.",
            to=[to_email],
        )
        email.send()
        return instance


class AchievementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Achievement
        fields = ["id", "title", "comment"]

    def __str__(self):
        return self.title


class UserSerializer(serializers.ModelSerializer):
    achieve = AchievementSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "username",
            "image",
            "experiment",
            "max_experiment",
            "level",
            "day",
            "wear_achievement",
            "achieve",
            "followings",
            "followers",
        ]

    def create(self, validated_data):
        validated_data["is_active"] = False
        user = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()

        uidb64 = urlsafe_base64_encode(force_bytes(user.id))
        token = user_email_verify_token.make_token(user)
        to_email = user.email
        email = EmailMessage(
            f"<한> {user.username}님의 계정 인증",
            f"아래의 링크를 누르면 이메일 인증이 완료됩니다. \n\nhttp://127.0.0.1:8000/users/verify/{uidb64}/{token}",
            to=[to_email],
        )
        email.send()
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get("username", instance.username)
        instance.image = validated_data.get("image", instance.image)
        instance.wear_achievement = validated_data.get(
            "wear_achievement", instance.wear_achievement
        )
        instance.save()
        return instance


class UserBattleSerializer(serializers.ModelSerializer):
    achieve = AchievementSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "username",
            "image",
            "experiment",
            "level",
            "day",
            "wear_achievement",
            "achieve",
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["username"] = user.username
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        request = self.context["request"]
        request.session.save()

        data["session_data"] = request.session.session_key

        return data


class RankingSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "image",
            "experiment",
            "level",
            "day",
            "wear_achievement",
            "achieve",
        ]
