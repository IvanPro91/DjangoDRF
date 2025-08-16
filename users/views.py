from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from users.filters import PayFilter
from users.models import Pay
from users.serializers import PaySerializer


# Create your views here.
class PayViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Вьюсет для отображения платежей.
    Поддерживает:
    - фильтрацию по курсу, уроку, способу оплаты,
    - сортировку по дате оплаты (возрастание/убывание).
    """
    queryset = Pay.objects.all()
    serializer_class = PaySerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = PayFilter
    ordering_fields = ['date_pay']
    ordering = ['-date_pay']  # по умолчанию — новые сверху