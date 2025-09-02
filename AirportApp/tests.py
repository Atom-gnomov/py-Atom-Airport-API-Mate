from django.test import TestCase

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Airport, AirplaneType, Airplane, Route, Flight, Order, Ticket
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta


class AirportAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        self.airport1 = Airport.objects.create(name="Airport 1", closest_biggest_city="City A")
        self.airport2 = Airport.objects.create(name="Airport 2", closest_biggest_city="City B")
        self.airplane_type = AirplaneType.objects.create(name="Boeing 737")
        self.airplane = Airplane.objects.create(name="Plane 1", rows=20, seats_in_row=6,
                                                airplane_type=self.airplane_type)
        self.route = Route.objects.create(source=self.airport1, destination=self.airport2, distance=500)
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now() + timedelta(days=1),
            arrival_time=timezone.now() + timedelta(days=1, hours=2)
        )

    def test_get_airports(self):
        url = "/api/v1/airports/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_order_and_tickets(self):
        url = "/api/v1/orders/"
        data = {"flight": self.flight.id, "quantity": 3}  # Assuming your endpoint accepts quantity
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Ticket.objects.count(), 3)

    def test_get_flights_with_filter(self):
        url = f"/api/v1/flights/?route={self.route.id}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_order_requires_authentication(self):
        self.client.credentials()  # Remove token
        url = "/api/v1/orders/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_airport(self):
        url = "/api/v1/airports/"
        data = {"name": "Airport 3", "closest_biggest_city": "City C"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Airport.objects.count(), 3)

class AdditionalAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser2", password="testpass2")
        self.client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

        # Setup models
        self.airport = Airport.objects.create(name="Airport X", closest_biggest_city="City X")
        self.airplane_type = AirplaneType.objects.create(name="Airbus A320")
        self.airplane = Airplane.objects.create(
            name="Plane X", rows=25, seats_in_row=6, airplane_type=self.airplane_type
        )
        self.route = Route.objects.create(source=self.airport, destination=self.airport, distance=1000)
        self.flight = Flight.objects.create(
            route=self.route,
            airplane=self.airplane,
            departure_time=timezone.now() + timedelta(days=2),
            arrival_time=timezone.now() + timedelta(days=2, hours=3)
        )
        self.crew_member = Crew.objects.create(first_name="John", second_name="Doe")
        self.flight.crew.add(self.crew_member)
        self.order = Order.objects.create(user=self.user)
        self.ticket = Ticket.objects.create(row=1, seat=1, flight=self.flight, order=self.order)

    def test_list_tickets(self):
        url = "/api/v1/tickets/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_ticket(self):
        url = "/api/v1/tickets/"
        data = {"row": 2, "seat": 2, "flight": self.flight.id, "order": self.order.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ticket.objects.count(), 2)

    def test_list_crew(self):
        url = "/api/v1/crew/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], "John")

    def test_create_crew_member(self):
        url = "/api/v1/crew/"
        data = {"first_name": "Jane", "second_name": "Smith"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Crew.objects.count(), 2)

    def test_list_airplane_types(self):
        url = "/api/v1/airplane-types/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_airplane_type(self):
        url = "/api/v1/airplane-types/"
        data = {"name": "Boeing 777"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(AirplaneType.objects.count(), 2)
