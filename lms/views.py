from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticated

from lms.models import Course, Lesson
from lms.paginations import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer
from users.permissions import IsOwner, ModeratorPermissions


class CoursesViewSet(viewsets.ModelViewSet):
    """Контролер отображения фильтрации и сортировки"""

    queryset = Course.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name"]
    ordering = ["-name"]
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return qs
        return qs.filter(owner=user)

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~ModeratorPermissions,
            )
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (
                IsAuthenticated,
                ModeratorPermissions | IsOwner,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                IsOwner,
            )
        return super().get_permissions()


class LessonsViewSet(viewsets.ModelViewSet):
    """Контролер отображения фильтрации и сортировки"""

    queryset = Lesson.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["name"]
    ordering = ["-name"]
    serializer_class = LessonSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.groups.filter(name="moders").exists():
            return qs
        return qs.filter(owner=user)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (
                IsAuthenticated,
                ~ModeratorPermissions,
            )
        elif self.action in ["update", "partial_update", "retrieve"]:
            self.permission_classes = (
                IsAuthenticated,
                ModeratorPermissions | IsOwner,
            )
        elif self.action == "destroy":
            self.permission_classes = (
                IsAuthenticated,
                IsOwner,
            )
        return super().get_permissions()
