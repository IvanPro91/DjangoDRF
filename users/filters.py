import django_filters

from lms.models import Course, Lesson
from users.models import Pay


class PayFilter(django_filters.FilterSet):
    lesson = django_filters.ModelChoiceFilter(field_name="lesson", queryset=Lesson.objects.all(), label="Урок")
    course = django_filters.ModelChoiceFilter(field_name="course", queryset=Course.objects.all(), label="Курс")
    type_pay = django_filters.ChoiceFilter(field_name="type_pay", choices=Pay.STATUS_CHOICES, label="Вид оплаты")

    class Meta:
        model = Pay
        fields = ["course", "lesson", "type_pay"]
