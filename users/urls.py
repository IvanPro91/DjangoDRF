from rest_framework.routers import DefaultRouter

from .apps import UsersConfig
from .views import PayViewSet

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'payments', PayViewSet)

urlpatterns = router.urls