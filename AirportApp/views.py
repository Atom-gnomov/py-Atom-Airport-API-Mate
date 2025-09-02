import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Crew, Ticket, Airport, Airplane, AirplaneType, Route, Flight, Order
from .serializers import AirportSerializer, CrewSerializer, AirplaneTypeSerializer, AirplaneSerializer, \
    AirplaneDetailSerializer, AirplaneListSerializer, RouteSerializer, RouteListSerializer, RouteDetailSerializer, \
    FlightSerializer, FlightListSerializer, FlightDetailSerializer, OrderSerializer, OrderDetailSerializer, \
    OrderListSerializer, TicketSerializer, TicketListSerializer, TicketDetailSerializer, UserSerializer, \
    AutoOrderSerializer
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.settings import api_settings

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all().prefetch_related()
    serializer_class = AirportSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name', 'closest_biggest_city']



class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all().prefetch_related()
    serializer_class = CrewSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['first_name', 'second_name']

class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all().prefetch_related()
    serializer_class = AirplaneTypeSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name']


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all().prefetch_related()
    serializer_class = AirplaneSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['name', 'airplane_type']
    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        if self.action == "retrieve":
            return AirplaneDetailSerializer
        return AirplaneSerializer

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all()
    serializer_class = RouteSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['source','destination']
    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        elif self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().prefetch_related()
    serializer_class = FlightSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['route','airplane']
    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        elif self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().prefetch_related()
    serializer_class = OrderSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        elif self.action == "retrieve":
            return OrderDetailSerializer
        if self.action == "create":
            return AutoOrderSerializer
        return OrderSerializer

class TicketViewSet(viewsets.ModelViewSet,generics.ListAPIView):
    queryset = Ticket.objects.all().prefetch_related()
    serializer_class = TicketSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['row','seat','flight','order']
    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        elif self.action == "retrieve":
            return TicketDetailSerializer
        return TicketSerializer


class CreateUserView(generics.CreateAPIView):
    permission_classes = []
    serializer_class = UserSerializer

class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = [AllowAny]
class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user