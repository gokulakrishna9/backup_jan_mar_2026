# online-shopping

Generated Spring WebFlux Application

## Build

```bash
mvn clean install
```

## Run

```bash
mvn spring-boot:run
```

## API Documentation

Swagger UI: http://localhost:8081/swagger-ui.html

## Database

- Type: mysql
- Host: localhost
- Port: 3306
- Database: online_shopping

## Authentication

This application uses JWT authentication. Register a user and login to get a JWT token.

### Register

```bash
POST /api/auth/register
{
  "username": "user@example.com",
  "password": "password123",
  "role": "USER"
}
```

### Login

```bash
POST /api/auth/login
{
  "username": "user@example.com",
  "password": "password123"
}
```

Use the returned JWT token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Authorization

This application implements entity-level authorization with access levels:
- READ (1)
- CREATE (2)
- UPDATE (3)
- DELETE (4)
- ADMIN (5)

Higher levels include all lower level permissions.
