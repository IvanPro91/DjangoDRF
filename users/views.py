from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from users.filters import PayFilter
from users.models import Pay, User
from users.serializers import PaySerializer, UserCreateSerializer, UserDetailViewSerializer, UserViewSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        user = serializer.save(is_active = True)
        user.set_password(user.password)
        user.save()


class PayViewSet(viewsets.ReadOnlyModelViewSet):
    """Контролеер отображения фильтрации и сортировки"""

    queryset = Pay.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PayFilter
    ordering_fields = ["date_pay"]
    ordering = ["-date_pay"]

    serializer_class = PaySerializer


class UserViewSet(viewsets.ModelViewSet):
    """Контролер CRUD пользователей"""

    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ["email"]
    ordering = ["-email"]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailViewSerializer
        return UserViewSerializer

