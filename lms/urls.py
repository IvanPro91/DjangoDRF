from rest_framework.routers import SimpleRouter
from lms.apps import LmsConfig
from lms.views import CourseViewSet

app_name = LmsConfig.name

route = SimpleRouter()
route.register('', CourseViewSet)

urlpatterns = []
urlpatterns += route.urls