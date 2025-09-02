from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Crew, Ticket, Airport, Airplane, AirplaneType, Route, Flight, Order


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = '__all__'


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = '__all__'


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = '__all__'


class RouteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Route
        fields = '__all__'



class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ("created_at", "user")

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class OrderListSerializer(OrderSerializer):
    class Meta(OrderSerializer.Meta):
        fields = ("id", "created_at")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email")
        read_only_fields = ("id", "username", "email")

class OrderDetailSerializer(OrderSerializer):
    user = UserSerializer(read_only=True)


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'


class AirplaneListSerializer(serializers.ModelSerializer):
    airplane_type = serializers.StringRelatedField()

    class Meta:
        model = Airplane
        fields = ("id", "name", "airplane_type", "rows", "seats_in_row")

class AirplaneDetailSerializer(serializers.ModelSerializer):
    airplane_type = AirplaneTypeSerializer(read_only=True)

    class Meta:
        model = Airplane
        fields = "__all__"


class RouteListSerializer(serializers.ModelSerializer):
    source = serializers.StringRelatedField()
    destination = serializers.StringRelatedField()

    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteDetailSerializer(serializers.ModelSerializer):
    source = AirportSerializer(read_only=True)
    destination = AirportSerializer(read_only=True)

    class Meta:
        model = Route
        fields = "__all__"


class FlightListSerializer(serializers.ModelSerializer):
    route = serializers.StringRelatedField()
    airplane = serializers.StringRelatedField()

    class Meta:
        model = Flight
        fields = ("id", "route", "airplane", "departure_time", "arrival_time")


class FlightDetailSerializer(serializers.ModelSerializer):
    route = RouteDetailSerializer(read_only=True)
    airplane = AirplaneSerializer(read_only=True)
    crew = CrewSerializer(many=True, read_only=True)

    class Meta:
        model = Flight
        fields = '__all__'


class TicketListSerializer(serializers.ModelSerializer):
    flight = FlightDetailSerializer(read_only=True)
    order = serializers.StringRelatedField()

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")


class TicketDetailSerializer(serializers.ModelSerializer):
    flight = FlightListSerializer(read_only=True)
    order = OrderSerializer(read_only=True)

    class Meta:
        model = Ticket
        fields = "__all__"


class AutoOrderSerializer(serializers.ModelSerializer):
    flight_id = serializers.IntegerField(write_only=True)
    passenger_count = serializers.IntegerField(write_only=True, default=1)

    class Meta:
        model = Order
        fields = ("id", "created_at", "user", "flight_id", "passenger_count")
        read_only_fields = ("id", "created_at", "user")

    def create(self, validated_data):
        user = self.context["request"].user
        flight_id = validated_data.pop("flight_id")
        passenger_count = validated_data.pop("passenger_count", 1)

        try:
            flight = Flight.objects.select_related("airplane").get(id=flight_id)
        except Flight.DoesNotExist:
            raise ValidationError("Flight not found.")

        airplane = flight.airplane
        max_seats = airplane.rows * airplane.seats_in_row

        # Get already booked seats
        occupied = Ticket.objects.filter(flight=flight).values_list("row", "seat")
        occupied_set = set(occupied)

        # Find free seats
        free_seats = []
        for r in range(1, airplane.rows + 1):
            for s in range(1, airplane.seats_in_row + 1):
                if (r, s) not in occupied_set:
                    free_seats.append((r, s))
                    if len(free_seats) >= passenger_count:
                        break
            if len(free_seats) >= passenger_count:
                break

        if len(free_seats) < passenger_count:
            raise ValidationError("Not enough free seats available on this flight.")

        with transaction.atomic():
            order = Order.objects.create(user=user)
            tickets = [
                Ticket(order=order, flight=flight, row=row, seat=seat)
                for row, seat in free_seats
            ]
            Ticket.objects.bulk_create(tickets)

        return order