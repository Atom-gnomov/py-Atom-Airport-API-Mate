from django.contrib import admin

from AirportApp.models import Order, Flight, AirplaneType, Airplane, Ticket, Crew, Airport, Route

admin.site.register(Crew)
admin.site.register(Ticket)
admin.site.register(Airport)
admin.site.register(Airplane)
admin.site.register(AirplaneType)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(Order)
