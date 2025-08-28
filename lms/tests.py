from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class LessonTestCase(APITestCase):
    BASE_URL_API = "http://127.0.0.1:8000"

    def setUp(self):
        self.user = User.objects.create(email="1@1.ru")
        self.course = Course.objects.create(name="Test Course", owner=self.user)
        self.lesson = Lesson.objects.create(name="Test Lesson", course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_user_subscribe(self):
        data = {'course_id': 2}
        response = self.client.post(f'{self.BASE_URL_API}/users/subscribe/', data)
        self.assertEqual(response.status_code, 200)

    def test_crud_lesson(self):
        # list lesson
        response = self.client.get(f'{self.BASE_URL_API}/lms/lessons/')
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        assert response.json() == {'count': 1, 'next': None, 'previous': None, 'results': [
            {'id': 1, 'name': 'Test Lesson', 'description': None, 'preview': None, 'video_url': None}]}
        # detail lesson
        response = self.client.get(f'{self.BASE_URL_API}/lms/lessons/1/')
        assert response.json() == {'id': 1, 'name': 'Test Lesson', 'description': None, 'preview': None,
                                   'video_url': None}
        # create lesson - invalid url
        response = self.client.post(f'{self.BASE_URL_API}/lms/lessons/',
                                    {"name": "test2", "course": 1,
                                     "owner": self.user, "video_url": "www.fsfsf.com"})
        assert response.json() == {'video_url': ["Ссылка должна вести на ресурсы: 'youtube.com'"]}
        # create lesson - valid url
        response = self.client.post(f'{self.BASE_URL_API}/lms/lessons/',
                                    {"name": "test2", "course": 1,
                                     "owner": self.user, "video_url": "www.youtube.com"})

        assert response.json() == {'id': 2, 'name': 'test2', 'description': None, 'preview': None,
                                   'video_url': 'www.youtube.com'}
        # update lesson
        response = self.client.put(f'{self.BASE_URL_API}/lms/lessons/2/',
                                   {"name": "test_test", 'video_url': 'www.youtube.com'})
        assert response.json() == {'id': 2, 'name': 'test_test', 'description': None, 'preview': None,
                                   'video_url': 'www.youtube.com'}
        # delete lesson
        self.client.delete(f'{self.BASE_URL_API}/lms/lessons/2/')
        response = self.client.get(f'{self.BASE_URL_API}/lms/lessons/')
        assert response.json().get("count") == 1
