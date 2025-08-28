from rest_framework import serializers

from lms.models import Course, Lesson
from lms.validators import validation_url


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Урока (Lesson).
    Используется как вложенный сериализатор в CourseSerializer.
    """
    video_url = serializers.CharField(validators=[validation_url])

    class Meta:
        model = Lesson
        fields = ["id", "name", "description", "preview", "video_url"]


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Курса (Course).

    Выводит:
    основную информацию о курсе,
    список всех уроков курса (вложенные данные),
    общее количество уроков в курсе.
    """

    lessons = LessonSerializer(many=True, read_only=True)
    lessons_count = serializers.SerializerMethodField(read_only=True)

    def get_lessons_count(self, obj):
        """Возвращает количество уроков, связанных с курсом."""
        return obj.payments.count()

    class Meta:
        model = Course
        fields = ["id", "name", "preview", "description", "lessons_count", "lessons"]
