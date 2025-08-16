import django_filters

from lms.models import Course, Lesson
from users.models import Pay


class PayFilter(django_filters.FilterSet):
    """
    Фильтр для модели Pay (платежи).
    Позволяет фильтровать:
    - по курсу,
    - по уроку,
    - по способу оплаты,
    а также сортировать по дате оплаты.
    """

    course = django_filters.ModelChoiceFilter(
        field_name='course',
        queryset=Course.objects.all(),
        label="Курс"
    )
    lesson = django_filters.ModelChoiceFilter(
        field_name='lesson',
        queryset=Lesson.objects.all(),
        label="Урок"
    )
    type_pay = django_filters.ChoiceFilter(
        field_name='type_pay',
        choices=Pay.STATUS_CHOICES,
        label="Способ оплаты"
    )

    class Meta:
        model = Pay
        fields = ['course', 'lesson', 'type_pay']