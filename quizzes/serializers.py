from rest_framework import serializers
from quizzes.models import *


class QuizSuggestSerializer(serializers.ModelSerializer):
    """퀴즈 시리얼라이저

    퀴즈를 제안 받을때 사용됩니다.
    """

    class Meta:
        model = UserQuiz
        fields = "__all__"


class OptionSerializer(serializers.ModelSerializer):
    """보기 시리얼라이저

    퀴즈를 제안 받을때와
    퀴즈를 제공 할때 보기를 처리합니다.
    """

    class Meta:
        model = UserQuizoption
        fields = (
            "content",
            "is_answer",
        )


class QuizSerializer(serializers.ModelSerializer):
    """퀴즈 제공 시리얼라이저

    퀴즈를 제공할때 사용됩니다.
    퀴즈마다 보기도 함께 제공합니다.
    """

    options = OptionSerializer(many=True)

    class Meta:
        model = UserQuiz
        fields = "__all__"


class QuizResultSerializer(serializers.Serializer):
    """퀴즈 결과 시리얼라이저

    퀴즈풀이 결과를 받을때 사용됩니다.
    """

    crossword = serializers.BooleanField(required=False)
    solved = serializers.BooleanField()


class QuizReportSerializer(serializers.ModelSerializer):
    """퀴즈 신고 시리얼라이저

    퀴즈 신고를 받을때 사용됩니다.
    """

    class Meta:
        model = QuizReport
        fields = (
            "user",
            "content",
            "quiz_type",
            "quiz_content",
        )
