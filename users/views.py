from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets

from users.filters import PayFilter
from users.models import Pay
from users.serializers import PaySerializer


class PayViewSet(viewsets.ReadOnlyModelViewSet):
    """Контролеер отображения фильтрации и сортировки"""

    queryset = Pay.objects.all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = PayFilter
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    serializer_class = PaySerializer
