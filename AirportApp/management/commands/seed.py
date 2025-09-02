from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from django.utils import timezone
from datetime import timedelta
import random

from AirportApp.models import Ticket, Order, Flight, AirplaneType, Airplane, Route, Airport, Crew


class Command(BaseCommand):
    help = "Seed database with test data for development"

    def handle(self, *args, **options):
        # Clear old data (optional)
        Ticket.objects.all().delete()
        Order.objects.all().delete()
        Flight.objects.all().delete()
        Airplane.objects.all().delete()
        AirplaneType.objects.all().delete()
        Route.objects.all().delete()
        Airport.objects.all().delete()
        Crew.objects.all().delete()
        User.objects.all().exclude(is_superuser=True).delete()

        self.stdout.write(self.style.WARNING("Deleted old test data."))

        # Create users
        users = []
        for i in range(3):
            user = User.objects.create_user(
                username=f"user{i+1}",
                password="test1234"
            )
            users.append(user)
        self.stdout.write(self.style.SUCCESS("Created users."))

        # Create crew
        crew_members = []
        for i in range(5):
            c = Crew.objects.create(first_name=f"Crew{i+1}", second_name="Member")
            crew_members.append(c)
        self.stdout.write(self.style.SUCCESS("Created crew."))

        # Airports
        kyiv = Airport.objects.create(name="Kyiv Boryspil", closest_biggest_city="Kyiv")
        lviv = Airport.objects.create(name="Lviv Danylo Halytskyi", closest_biggest_city="Lviv")
        odessa = Airport.objects.create(name="Odesa Intl", closest_biggest_city="Odesa")

        # Routes
        r1 = Route.objects.create(source=kyiv, destination=lviv, distance=540)
        r2 = Route.objects.create(source=lviv, destination=odessa, distance=620)
        r3 = Route.objects.create(source=odessa, destination=kyiv, distance=480)

        self.stdout.write(self.style.SUCCESS("Created airports and routes."))

        # Airplane types
        boeing = AirplaneType.objects.create(name="Boeing 737")
        airbus = AirplaneType.objects.create(name="Airbus A320")

        # Airplanes
        a1 = Airplane.objects.create(name="UR-AAA", rows=20, seats_in_row=6, airplane_type=boeing)
        a2 = Airplane.objects.create(name="UR-BBB", rows=25, seats_in_row=6, airplane_type=airbus)

        self.stdout.write(self.style.SUCCESS("Created airplanes."))

        # Flights
        now = timezone.now()
        flights = []
        for idx, route in enumerate([r1, r2, r3], start=1):
            f = Flight.objects.create(
                route=route,
                airplane=random.choice([a1, a2]),
                departure_time=now + timedelta(days=idx),
                arrival_time=now + timedelta(days=idx, hours=2),
            )
            f.crew.set(random.sample(crew_members, 2))
            flights.append(f)

        self.stdout.write(self.style.SUCCESS("Created flights."))

        # Orders + Tickets
        for user in users:
            order = Order.objects.create(user=user)
            for flight in flights:
                # choose random seat
                row = random.randint(1, flight.airplane.rows)
                seat = random.randint(1, flight.airplane.seats_in_row)
                Ticket.objects.create(row=row, seat=seat, flight=flight, order=order)

        self.stdout.write(self.style.SUCCESS("Created orders and tickets."))

        self.stdout.write(self.style.SUCCESS("✅ Test data seeded successfully!"))
