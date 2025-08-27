from rest_framework.routers import DefaultRouter
from .views import AirportViewSet, CrewViewSet, AirplaneTypeViewSet, AirplaneViewSet
app_name = "AirportApp"
router = DefaultRouter()
router.register(r'airports', AirportViewSet)
router.register(r'crew', CrewViewSet)
router.register(r'airplane-types', AirplaneTypeViewSet)
router.register(r'airplanes', AirplaneViewSet)

urlpatterns = router.urls