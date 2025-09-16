# Car Rental API - Tech Test

A simple REST API for a car rental service, built with FastAPI.

## Features

- ✅ List available cars for a specific date
- ✅ Create bookings with availability validation  
- ✅ Key event logging
- ✅ Basic integration tests
- ✅ JSON file storage
- ✅ Dockerization

## Project Structure

```bash
C:.
├───app
│   ├───api 
│   │   └───routes  # FastAPI Endpoints
│   ├───core
│   │   ├───logger  # Logging
│   │   ├───models  # Data models
│   │   └───services  # Business logic
│   ├───data  # JSON database
│   ├───infra  # Infrastructure implementation
│   └───test  # Integration tests
│   └───main.py  # Main application
│   Dockerfile # Dockerfile
│   requirements.txt # Dependencies
└───logs  # Application logs
```

## Usage Instructions

```bash
git clone https://github.com/blasd/bookline.git
cd bookline
docker build -t car-rental-api .
docker run -p 8000:8000 -v ${PWD}:/app --name car-api car-rental-api
```

## Access the API:

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs

## Endpoints

**List available cars for a specific date**
- GET /cars/available?date=2025-09-16

**List all cars**
- GET /cars

**List all bookings** 
- GET /bookings

**Create a booking**
- POST /bookings

## Basic Integration Tests

```bash
python -m pytest app/test/ -v
```

## Design Decisions

- FastAPI: Modern framework with automatic validation and interactive documentation
- JSON file: Simplicity for the test, easy to replace with real database
- Docker: Containerization for development and production environments
- Logging: Key event logging for debugging and monitoring
- Tests: Basic integration tests to verify endpoints work correctly
- Clear and modular project structure
- Separation of concerns: Services, routes and models separated

## Development Time

3 hours

## Possible Application Improvements

- Robust validations
- More unit tests
- Concurrency handling
- Real database implementation
- Authentication and authorization
- Rate limiting
- API versioning
- Comprehensive error handling
- Performance optimization
- Monitoring and metrics