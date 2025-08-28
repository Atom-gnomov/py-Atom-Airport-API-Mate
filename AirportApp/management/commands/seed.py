from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from AirportApp.models import Airport, AirplaneType, Airplane, Crew, Route, Flight, Order, Ticket
import random
from datetime import timedelta


class Command(BaseCommand):
    help = "Seed database with demo data"

    def handle(self, *args, **kwargs):
        # Create demo user
        User = get_user_model()
        user, created = User.objects.get_or_create(username="demo_user", defaults={"password": "demo12345"})
        if created:
            self.stdout.write(self.style.SUCCESS(f"Created user {user.username}"))

        # Create airports
        airports = [
            ("JFK International", "New York"),
            ("LAX International", "Los Angeles"),
            ("Heathrow", "London"),
            ("Haneda", "Tokyo"),
        ]
        airport_objs = []
        for name, city in airports:
            obj, _ = Airport.objects.get_or_create(name=name, closest_biggest_city=city)
            airport_objs.append(obj)

        # Create airplane types
        airplane_types = ["Boeing 737", "Airbus A320", "Embraer E190"]
        type_objs = []
        for t in airplane_types:
            obj, _ = AirplaneType.objects.get_or_create(name=t)
            type_objs.append(obj)

        # Create airplanes
        airplanes = [
            ("BoeingOne", 20, 6, type_objs[0]),
            ("AirbusFast", 25, 6, type_objs[1]),
            ("EmbraerSmall", 15, 4, type_objs[2]),
        ]
        airplane_objs = []
        for name, rows, seats, atype in airplanes:
            obj, _ = Airplane.objects.get_or_create(name=name, rows=rows, seats_in_row=seats, airplane_type=atype)
            airplane_objs.append(obj)

        # Create crew
        crew_members = [
            ("John", "Doe"),
            ("Jane", "Smith"),
            ("Alex", "Brown"),
        ]
        crew_objs = []
        for fn, ln in crew_members:
            obj, _ = Crew.objects.get_or_create(first_name=fn, second_name=ln)
            crew_objs.append(obj)

        # Create routes
        route_objs = []
        for i in range(len(airport_objs)):
            for j in range(len(airport_objs)):
                if i != j:
                    obj, _ = Route.objects.get_or_create(
                        source=airport_objs[i],
                        destination=airport_objs[j],
                        defaults={"distance": random.randint(500, 5000)},
                    )
                    route_objs.append(obj)

        # Create flights
        flight_objs = []
        for i in range(5):
            route = random.choice(route_objs)
            airplane = random.choice(airplane_objs)
            departure = timezone.now() + timedelta(days=i)
            arrival = departure + timedelta(hours=random.randint(2, 10))
            flight = Flight.objects.create(
                route=route,
                airplane=airplane,
                departure_time=departure,
                arrival_time=arrival,
            )
            flight.crew.set(random.sample(crew_objs, k=2))
            flight_objs.append(flight)




        self.stdout.write(self.style.SUCCESS("Database seeded successfully ✅"))
