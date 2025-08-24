from django.core.management import BaseCommand

from lms.models import Course, Lesson
from users.models import Pay, User


class Command(BaseCommand):
    help = "Засеивание БД тестовыми данными"
    users_test_data = [
        {
            "email": "admin@admin.com",
            "is_staff": True,
            "is_active": True,
            "is_superuser": True,
            "password": "1234",
        },
        {
            "email": "1@admin.com",
            "is_staff": True,
            "is_active": True,
            "is_superuser": False,
            "password": "1234",
        },
        {
            "email": "2@admin.com",
            "is_staff": True,
            "is_active": True,
            "is_superuser": False,
            "password": "1234",
        },
    ]

    def handle(self, *args, **kwargs):
        course = Course.objects.create(name="Урок Python", description="Базовые функции Python")
        lesson = Lesson.objects.create(name="Переменные", description="Переменные в Python", course=course)

        for data_user in self.users_test_data:
            get_user = User.objects.filter(email=data_user["email"]).first()
            if not get_user:
                user: User = User.objects.create(
                    email=data_user["email"],
                    is_staff=data_user["is_staff"],
                    is_active=data_user["is_active"],
                    is_superuser=data_user["is_superuser"],
                )
                user.set_password(data_user["password"])
                user.save()

                if not data_user["is_superuser"]:
                    Pay.objects.create(user=user, lesson=lesson, course=course, money=11232, type_pay=Pay.TYPE_CASH)
        self.stdout.write(self.style.SUCCESS("Засеивание выполнено успешно"))
