# CAMPUS_API
A production-ready Flask REST API application containerized using Docker to ensure environment consistency. The project demonstrates backend development best practices including modular architecture, dependency management, and container-based deployment. It is designed to run seamlessly across local development environments and cloud platforms .
See live at https://campus-api-4nik.onrender.com/apidocs/
# Campus Management API

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-REST%20API-green)
![JWT](https://img.shields.io/badge/Auth-JWT-orange)
![Docker](https://img.shields.io/badge/Container-Docker-blue)
![Render](https://img.shields.io/badge/Deployment-Render-purple)

A Flask-based REST API for managing students, departments, and authentication in a campus management system.

---

# Live Deployment

### API Base URL

https://campus-api-4nik.onrender.com/

### Swagger Documentation

https://campus-api-4nik.onrender.com/apidocs/

You can explore and test all API endpoints directly using Swagger UI.

---

# Features

## Authentication & Authorization

* User Registration
* User Login
* JWT Authentication
* Refresh Tokens
* User Profile
* Change Password
* Logout with Token Revocation
* Role-Based Access Control

## Student Management

* Add Students
* View Students
* Pagination
* Department Mapping
* Input Validation
* Duplicate Email Detection

## Department Management

* Add Departments
* View Departments

## Security

* Password Hashing
* JWT Access Tokens
* JWT Refresh Tokens
* Token Blacklisting
* Rate Limiting
* Environment Variables
* Request Logging

## Documentation

* Swagger UI using Flasgger

## Testing

* Pytest
* Coverage Reports
* Authentication Tests
* Student API Tests

---

# Tech Stack

## Backend

* Python
* Flask

## Database

* SQLite
* SQLAlchemy ORM

## Authentication

* Flask-JWT-Extended

## Documentation

* Flasgger (Swagger)

## Validation

* Marshmallow

## Testing

* Pytest
* Pytest-Cov

## Database Migration

* Flask-Migrate
* Alembic

## Containerization

* Docker

## Deployment

* Render

---

# Project Structure

```text
campus-api/
│
├── app.py
├── config.py
├── models.py
├── auth_routes.py
├── extensions.py
├── requirements.txt
├── Dockerfile
├── .env
│
├── routes/
│   ├── student_routes.py
│   └── department_routes.py
│
├── schemas/
│   ├── student_schema.py
│   ├── login_schema.py
│   └── register_schema.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_student.py
│
├── migrations/
│
├── app.log
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone https://github.com/RAVINAMITTAL/CAMPUS_API.git

cd CAMPUS_API
```

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / Mac

```bash
source .venv/bin/activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file:

```env
JWT_SECRET_KEY=your_super_secret_key_here
```

Example:

```env
JWT_SECRET_KEY=campus_management_super_secret_key_2026_very_long_random_string
```

---

# Database Migration

Create migration:

```bash
flask db migrate -m "Initial Migration"
```

Apply migration:

```bash
flask db upgrade
```

---

# Run Application

```bash
python app.py
```

Application runs on:

```text
http://localhost:5000
```

---

# API Endpoints

## Authentication

| Method | Endpoint                     |
| ------ | ---------------------------- |
| POST   | /api/v1/auth/register        |
| POST   | /api/v1/auth/login           |
| GET    | /api/v1/auth/profile         |
| POST   | /api/v1/auth/logout          |
| PUT    | /api/v1/auth/change-password |
| POST   | /api/v1/auth/refresh         |

---

## Students

| Method | Endpoint                |
| ------ | ----------------------- |
| POST   | /api/v1/students/fill   |
| GET    | /api/v1/students/detail |

---

## Departments

| Method | Endpoint     |
| ------ | ------------ |
| POST   | /departments |
| GET    | /departments |

---

# Running Tests

Run all tests:

```bash
pytest -v
```

Generate coverage report:

```bash
coverage run -m pytest

coverage report -m
```

---

# Docker

## Build Docker Image

```bash
docker build -t campus-api .
```

## Run Container

```bash
docker run -p 5000:5000 campus-api
```

## Verify Running Container

```bash
docker ps
```

Open:

```text
http://localhost:5000
```

Swagger:

```text
http://localhost:5000/apidocs/
```

---

# Security Features

## Password Hashing

Passwords are hashed before storage using Werkzeug.

## JWT Authentication

Users receive:

* Access Token
* Refresh Token

after successful login.

## Token Revocation

Logged-out tokens are stored in a blacklist table and cannot be reused.

## Rate Limiting

Login endpoint protected against brute-force attacks:

```python
@limiter.limit("5 per minute")
```

## Logging

All incoming requests are logged using:

```python
@app.before_request
```

Logs are stored in:

```text
app.log
```

---

# Future Improvements

* PostgreSQL Integration
* Redis Rate Limiting
* Email Verification
* Forgot Password
* Docker Compose
* CI/CD with GitHub Actions
* Kubernetes Deployment
* User Activity Tracking
* Audit Logs

---

# Author

## Ravina Mittal

Backend Developer | Python | Flask | SQLAlchemy | JWT Authentication | Docker | REST APIs

### Project Links

GitHub Repository:
https://github.com/RAVINAMITTAL/CAMPUS_API

Live API:
https://campus-api-4nik.onrender.com/

Swagger Documentation:
https://campus-api-4nik.onrender.com/apidocs/

---

# License

This project is developed for educational and learning purposes.
