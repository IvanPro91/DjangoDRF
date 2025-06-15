from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", blank=False, null=False)
    preview = models.ImageField(upload_to='course/', verbose_name="Картинка")
    description = models.TextField(verbose_name="Описание")

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название", blank=False, null=False)
    preview = models.ImageField(upload_to='lesson/', verbose_name="Картинка")
    description = models.TextField(verbose_name="Описание")
    video_url = models.TextField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Курс")

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"