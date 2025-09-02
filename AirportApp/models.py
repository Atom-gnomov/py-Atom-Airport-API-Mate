from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)



    def __str__(self):
        return f"{self.first_name} {self.second_name}"


class Airport(models.Model):
    name = models.CharField(max_length=255, unique=True)
    closest_biggest_city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.closest_biggest_city})"


class AirplaneType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    distance = models.IntegerField()

    class Meta:
        unique_together = ("source", "destination")
        constraints = [
            models.CheckConstraint(
                check=~models.Q(source=models.F("destination")),
                name="prevent_same_airport_route",
            ),
            models.CheckConstraint(
                check=models.Q(distance__gt=0),
                name="distance_gt_zero",
            ),
        ]

    def __str__(self):
        return f"{self.source} → {self.destination}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        db_index=True,
    )

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class Airplane(models.Model):
    name = models.CharField(max_length=255, unique=True)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()
    airplane_type = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(rows__gt=0), name="rows_gt_zero"),
            models.CheckConstraint(check=models.Q(seats_in_row__gt=0), name="seats_gt_zero"),
        ]

    def __str__(self):
        return f"{self.name} ({self.airplane_type.name})"


class Flight(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    departure_time = models.DateTimeField(db_index=True)
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(
        Crew,
        blank=True,
        related_name="flights",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(arrival_time__gt=models.F("departure_time")),
                name="arrival_after_departure",
            )
        ]

    def __str__(self):
        return f"Flight {self.id} {self.route} at {self.departure_time}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("flight", "row", "seat")

    def clean(self):
        airplane = self.flight.airplane
        if self.row > airplane.rows or self.row <= 0:
            raise ValidationError("Row number is invalid for this airplane")
        if self.seat > airplane.seats_in_row or self.seat <= 0:
            raise ValidationError("Seat number is invalid for this airplane")

    def __str__(self):
        return f"Ticket {self.row}{self.seat} for flight {self.flight.id}"

