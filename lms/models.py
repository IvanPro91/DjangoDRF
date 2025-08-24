from django.db import models



class Course(models.Model):
    """
    Модель курса, представляющая образовательный курс в системе.

    Курс содержит название, изображение-превью и описание.
    Может включать в себя несколько уроков, связанных с ним.

    name (CharField): Название курса. Максимум 100 символов. Обязательное поле.
    preview (ImageField): Превью курса. Загружается в папку 'course/'.
    description (TextField): Описание курса. Может содержать подробную информацию.
    """

    name = models.CharField(max_length=100, verbose_name="Название", blank=False, null=False)
    preview = models.ImageField(upload_to="course/", verbose_name="Картинка")
    description = models.TextField(verbose_name="Описание")
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        """Определяет человекочитаемое имя модели и его множественную форму"""

        verbose_name = "Курс"
        verbose_name_plural = "Курсы"

    def __str__(self):
        """Возвращает строковое представление объекта Course."""
        return self.name


class Lesson(models.Model):
    """
    Модель урока, входящего в состав определённого курса.

    Урок содержит название, описание, превью и ссылку на видео.
    Связан с моделью Course через внешний ключ.

    name (CharField): Название урока. Максимум 100 символов. Обязательное поле.
    preview (ImageField): Превью урока. Загружается в папку 'lesson/'.
    description (TextField): Описание урока.
    video_url (TextField): Ссылка на видеоурок (например, YouTube или локальное хранилище).
    course (ForeignKey): Ссылка на курс, к которому относится урок.
    """

    name = models.CharField(max_length=100, verbose_name="Название", blank=False, null=False)
    preview = models.ImageField(upload_to="lesson/", verbose_name="Картинка")
    description = models.TextField(verbose_name="Описание")
    video_url = models.TextField(verbose_name="Ссылка на видео")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Курс")
    owner = models.ForeignKey('users.User', on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
        """Определяет человекочитаемое имя модели и его множественную форму"""

        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        """
        Возвращает строковое представление объекта Lesson.

        Returns:
            str: Название урока.
        """
        return self.name
