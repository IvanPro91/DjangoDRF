from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from lms.models import Course, Lesson
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import ModeratorPermissions, IsOwner


class CoursesViewSet(viewsets.ModelViewSet):
    """Контролер отображения фильтрации и сортировки"""

    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name"]
    ordering = ["-name"]

    def get_serializer_class(self):
        return CourseSerializer

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~ModeratorPermissions,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (ModeratorPermissions | IsOwner)
        elif self.action == 'destroy':
            self.permission_classes = (~ModeratorPermissions, IsOwner)
        elif self.action in ['update', 'destroy']:
            self.permission_classes = (ModeratorPermissions,)
        return super().get_permissions()

class LessonsViewSet(viewsets.ModelViewSet):
    """Контролер отображения фильтрации и сортировки"""

    queryset = Lesson.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name"]
    ordering = ["-name"]

    def get_serializer_class(self):
        return LessonSerializer

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (~ModeratorPermissions,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (ModeratorPermissions | IsOwner)
        elif self.action == 'destroy':
            self.permission_classes = (~ModeratorPermissions, IsOwner)
        elif self.action in ['update', 'destroy']:
            self.permission_classes = (ModeratorPermissions,)
        return super().get_permissions()

