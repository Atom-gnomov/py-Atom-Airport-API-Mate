from rest_framework.routers import DefaultRouter
from .views import AirportViewSet, CrewViewSet, AirplaneTypeViewSet, AirplaneViewSet, RouteViewSet, FlightViewSet, \
    OrderViewSet, TicketViewSet

app_name = "AirportApp"
router = DefaultRouter()
router.register(r'airports', AirportViewSet)
router.register(r'crew', CrewViewSet)
router.register(r'airplane-types', AirplaneTypeViewSet)
router.register(r'airplanes', AirplaneViewSet)
router.register(r'routes', RouteViewSet)
router.register(r'flights', FlightViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'tickets', TicketViewSet)
urlpatterns = router.urls