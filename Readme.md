# Airport API

A **Django REST API** for managing flights, airports, airplanes, routes, tickets, and orders, with JWT authentication and Swagger documentation.

---

## **Table of Contents**

- [Features](#features)  
- [Requirements](#requirements)  
- [Setup](#setup)  
- [Environment Variables](#environment-variables)  
- [Running with Docker](#running-with-docker)  
- [API Endpoints](#api-endpoints)  
- [Authentication](#authentication)  
- [Swagger Documentation](#swagger-documentation)  
- [Admin Panel](#admin-panel)

---

## **Features**

- Manage **Airports, Routes, Airplanes, Airplane Types, Crews, Flights, Orders, Tickets**.  
- Automatic ticket creation when creating an order based on available seats.  
- JWT authentication for secure API access.  
- Filtering support for Flights, Tickets, Orders, Airplanes, and Routes.  
- Swagger API documentation.  

---

## **Requirements**

- Docker & Docker Compose  
- Python 3.11 (for local development without Docker)  
- PostgreSQL (via Docker)  

---

## **Setup**

Clone the repository:

```bash
git clone <your-repo-url>
cd <your-project-folder>
```
## **Running with Docker**

Build and start the Docker containers:

```bash
docker-compose up --build

```
```markdown
## **Environment Variables**

Create a `.env` file in your project root or set these environment variables in your system:

```

# Django settings

DJANGO\_SECRET\_KEY=your\_super\_secret\_key
DJANGO\_DEBUG=True

# Database settings

DJANGO\_DB\_NAME=airport\_db
DJANGO\_DB\_USER=airport\_user
DJANGO\_DB\_PASSWORD=airport\_pass
DJANGO\_DB\_HOST=db
DJANGO\_DB\_PORT=5432

# Optional: for email or other services

EMAIL\_HOST=smtp.example.com
EMAIL\_PORT=587
EMAIL\_HOST\_USER=[your\_email@example.com](mailto:your_email@example.com)
EMAIL\_HOST\_PASSWORD=your\_email\_password
EMAIL\_USE\_TLS=True

```

These variables are used by Django to configure the database, secret key, and optional services. Make sure `.env` is included in `.gitignore` to keep secrets safe.
```
## **API Endpoints**

The base URL for the API is:http://localhost:8000/api/v1/


### **Airports**
- `GET /airports/` – List all airports  
- `POST /airports/` – Create a new airport  
- `GET /airports/<id>/` – Retrieve airport details  
- `PUT /airports/<id>/` – Update airport  
- `DELETE /airports/<id>/` – Delete airport  

### **Airplane Types**
- `GET /airplane-types/` – List all airplane types  
- `POST /airplane-types/` – Create a new airplane type  
- `GET /airplane-types/<id>/` – Retrieve type details  
- `PUT /airplane-types/<id>/` – Update type  
- `DELETE /airplane-types/<id>/` – Delete type  

### **Airplanes**
- `GET /airplanes/` – List airplanes  
- `POST /airplanes/` – Create airplane  
- `GET /airplanes/<id>/` – Retrieve airplane details  
- `PUT /airplanes/<id>/` – Update airplane  
- `DELETE /airplanes/<id>/` – Delete airplane  

### **Routes**
- `GET /routes/` – List routes  
- `POST /routes/` – Create route  
- `GET /routes/<id>/` – Retrieve route details  
- `PUT /routes/<id>/` – Update route  
- `DELETE /routes/<id>/` – Delete route  

### **Flights**
- `GET /flights/` – List flights  
- `POST /flights/` – Create flight  
- `GET /flights/<id>/` – Retrieve flight details  
- `PUT /flights/<id>/` – Update flight  
- `DELETE /flights/<id>/` – Delete flight  

### **Orders**
- `GET /orders/` – List orders  
- `POST /orders/` – Create order (auto-generates tickets)  
- `GET /orders/<id>/` – Retrieve order details  
- `PUT /orders/<id>/` – Update order  
- `DELETE /orders/<id>/` – Delete order  

### **Tickets**
- `GET /tickets/` – List tickets  
- `POST /tickets/` – Create ticket  
- `GET /tickets/<id>/` – Retrieve ticket details  
- `PUT /tickets/<id>/` – Update ticket  
- `DELETE /tickets/<id>/` – Delete ticket  

### **Crew**
- `GET /crew/` – List crew members  
- `POST /crew/` – Add new crew member  
- `GET /crew/<id>/` – Retrieve crew details  
- `PUT /crew/<id>/` – Update crew member  
- `DELETE /crew/<id>/` – Delete crew member  

```markdown
## **Authentication**

This API uses **JWT (JSON Web Tokens)** for authentication.  

### **Register a new user**
```

POST /register/
Content-Type: application/json

{
"username": "your\_username",
"password": "your\_password",
"email": "[your\_email@example.com](mailto:your_email@example.com)"
}

```

### **Obtain JWT Token**
```

POST /token/
Content-Type: application/json

{
"username": "your\_username",
"password": "your\_password"
}

````
Response:
```json
{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}
````

### **Refresh JWT Token**

```
POST /token/refresh/
Content-Type: application/json

{
    "refresh": "<refresh_token>"
}
```

Response:

```json
{
    "access": "<new_access_token>"
}
```

### **Verify JWT Token**

```
POST /token/verify/
Content-Type: application/json

{
    "token": "<access_token>"
}
```

Response:

* `200 OK` if valid
* `401 Unauthorized` if invalid

### **Access User Profile**

```
GET /me/
Authorization: Bearer <access_token>
```

Response:

```json
{
    "id": 1,
    "username": "your_username",
    "email": "your_email@example.com"
}
```

> **Note:** Include the `Authorization: Bearer <access_token>` header for all protected endpoints like flights, orders, and tickets.

```markdown
## **Swagger Documentation**

The API includes Swagger UI for interactive API documentation.  

### **Accessing Swagger UI**

After running the project, open the browser and go to:

```

[http://localhost:8000/swagger/](http://localhost:8000/swagger/)

````

You will see a fully interactive documentation page with all endpoints, request/response examples, and authentication options.

### **Features**
- View all available endpoints grouped by models (Airports, Airplanes, Routes, Flights, Orders, Tickets, Crew).  
- Execute API requests directly from the browser.  
- Include JWT token in the “Authorize” button to test protected endpoints.  

### **Setup**
Make sure you have `drf-yasg` installed:

```bash
pip install drf-yasg
````

Add it to `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    'drf_yasg',
]
```

In `urls.py`, add:

```python
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Airport API",
      default_version='v1',
      description="API documentation for Airport project",
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
```

After this, navigate to `/swagger/` to explore and test your API.

````markdown
## **Admin Panel**

Django provides a built-in **Admin Panel** to manage all models from a web interface.  

### **Accessing the Admin Panel**

1. Run your Django server:

```bash
python manage.py runserver
````

2. Open your browser and go to:

```
http://localhost:8000/admin/
```

3. Log in with a superuser account. If you don’t have one, create it:

```bash
python manage.py createsuperuser
```

### **Registering Models in Admin**

All models in the Airport API should be added to the admin panel. In `AirportApp/admin.py`:

```python
from django.contrib import admin
from .models import Airport, AirplaneType, Airplane, Route, Flight, Crew, Order, Ticket

admin.site.register(Airport)
admin.site.register(AirplaneType)
admin.site.register(Airplane)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(Crew)
admin.site.register(Order)
admin.site.register(Ticket)
```




