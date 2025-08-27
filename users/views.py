from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from lms.models import Course
from users.filters import PayFilter
from users.models import Pay, User, SubscribeUser
from users.serializers import PaySerializer, UserCreateSerializer, UserDetailViewSerializer, UserViewSerializer
from users.services import create_stripe_price_amount, create_stripe_session


def user_subscribe_course(request: Request):
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        user = request.user
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item: SubscribeUser = SubscribeUser.objects.filter(user=user, course=course_item).first()

        if subs_item:
            subs_item.delete()
            message = "Подписка удалена"
        else:
            SubscribeUser.objects.create(user=user, course=course_item)
            message = "Подписка оформлена"

        return Response({"message": message})

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (AllowAny, )

    def perform_create(self, serializer):
        user = serializer.save(is_active = True)
        user.set_password(user.password)
        user.save()

class CreateProductPrice(CreateAPIView):
    serializer_class = PaySerializer
    queryset = Pay.objects.all()

    def perform_create(self, serializer):
        pay = serializer.save(user = self.request.user)
        price = create_stripe_price_amount(pay.name_product, pay.amount)
        session_id, session_link = create_stripe_session(price)
        pay.session_id = session_id
        pay.link = session_link
        pay.save()
        # super().perform_create(serializer)


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

