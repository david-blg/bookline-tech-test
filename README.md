# Car Rental API - Tech Test

A clean and functional REST API for a car rental service, built with FastAPI following best practices and architectural patterns.

## Features

- ✅ List available cars for a specific date
- ✅ Create bookings with availability validation
- ✅ Comprehensive logging for key application events
- ✅ Unit and integration tests
- ✅ JSON file-based storage
- ✅ Docker containerization
- ✅ Clean architecture with separation of concerns

## Project Structure

```bash
C:.
├───app
│   ├───api
│   │   └───routes          # FastAPI route handlers
│   ├───core
│   │   ├───interfaces      # Repository interfaces
│   │   ├───logger          # Logging configuration
│   │   ├───models          # Pydantic data models
│   │   ├───repositories    # Data access layer
│   │   └───use_cases       # Business logic layer
│   ├───infra              # Infrastructure (database setup)
│   ├───test               # Test suite
│   └───main.py            # Application entry point
├───Dockerfile             # Container configuration
└───requirements.txt       # Python dependencies
```

## Quick Start

### Using Docker (Recommended)

```bash
git clone https://github.com/david-blg/bookline-tech-test bookline
cd bookline
docker build -t car-rental-api .
docker run -p 8000:8000 -v ${PWD}:/app --name car-api car-rental-api
```

### Local Development

```bash
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

## API Access

- **API Base URL**: http://localhost:8000
- **Interactive Documentation**: http://localhost:8000/docs
- **OpenAPI Schema**: http://localhost:8000/redoc

## API Endpoints

### List Available Cars
**GET** `/cars/available`
- **Query Parameters**: 
  - `target_date` (required): Date in YYYY-MM-DD format
- **Description**: Returns all cars available for booking on the specified date
- **Request Url**: `GET /cars/available?target_date=2025-09-20`

```bash
curl -X 'GET' \
  'http://localhost:8000/cars/available?target_date=2025-09-20' \
  -H 'accept: application/json'
```

### Create Booking
**POST** `/bookings`
- **Request Body**: JSON with car_id and booking_date
- **Description**: Creates a new booking if the car is available
- **Request Url**: `http://localhost:8000/bookings/`

```bash
curl -X 'POST' \
  'http://localhost:8000/bookings/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "car_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
  "customer_name": "string",
  "customer_email": "user@example.com",
  "start_date": "2025-09-20",
  "end_date": "2025-09-20"
}'
```

## Running Tests

Execute the test suite to verify functionality:

```bash
# Run all tests
pytest app/test/ -v
```

### Output

```bash
collected 9 items                                                                                                                                     

app/test/test_booking_endpoint.py::test_get_all_bookings PASSED                                                                                 [ 11%]
app/test/test_booking_endpoint.py::test_create_booking_success PASSED                                                                           [ 22%]
app/test/test_booking_endpoint.py::test_create_booking_invalid_dates PASSED                                                                     [ 33%]
app/test/test_booking_endpoint.py::test_create_booking_with_nonexist_car PASSED                                                                 [ 44%]
app/test/test_cars_endpoint.py::test_get_all_cars_success PASSED                                                                                [ 55%]
app/test/test_cars_endpoint.py::test_get_available_cars_for_valid_date PASSED                                                                   [ 66%]
app/test/test_cars_endpoint.py::test_get_available_cars_for_past_date PASSED                                                                    [ 77%]
app/test/test_cars_endpoint.py::test_get_available_cars_for_today PASSED                                                                        [ 88%] 
app/test/test_cars_endpoint.py::test_cars_response_structure PASSED                                                                             [100%]

================================================================= 9 passed in 0.67s ================================================================== 
```

# Run specific test files
pytest app/test/test_cars_endpoint.py -v
pytest app/test/test_booking_endpoint.py -v


### Test Cars Endpoint Output

```bash
collected 5 items                                                                                                                                     

app/test/test_cars_endpoint.py::test_get_all_cars_success PASSED                                                                                [ 20%]
app/test/test_cars_endpoint.py::test_get_available_cars_for_valid_date PASSED                                                                   [ 40%]
app/test/test_cars_endpoint.py::test_get_available_cars_for_past_date PASSED                                                                    [ 60%]
app/test/test_cars_endpoint.py::test_get_available_cars_for_today PASSED                                                                        [ 80%] 
app/test/test_cars_endpoint.py::test_cars_response_structure PASSED                                                                             [100%]

================================================================= 5 passed in 0.19s ================================================================== 
```

### Test Booking Endpoint Output

```bash
collected 4 items                                                                                                                                     

app/test/test_booking_endpoint.py::test_get_all_bookings PASSED                                                                                 [ 25%]
app/test/test_booking_endpoint.py::test_create_booking_success PASSED                                                                           [ 50%]
app/test/test_booking_endpoint.py::test_create_booking_invalid_dates PASSED                                                                     [ 75%]
app/test/test_booking_endpoint.py::test_create_booking_with_nonexist_car PASSED                                                                 [100%]

================================================================= 4 passed in 0.25s ================================================================== 
```

## Design Decisions

### Architecture
- **Clean Architecture**: Implemented with clear separation between API routes, business logic (use cases), and data access (repositories)
- **Dependency Injection**: Used FastAPI's dependency injection system for loose coupling
- **Interface Segregation**: Repository interfaces define contracts for data access

### Technology Choices
- **FastAPI**: Modern Python framework with automatic validation, serialization, and interactive documentation
- **Pydantic Models**: Strong typing and automatic validation for request/response data
- **JSON Storage**: File-based storage for simplicity, easily replaceable with database implementation

### Logging Strategy
- **Structured Logging**: Captures key application events including:
  - Successful and failed booking attempts
  - Available car queries
  - Application startup and configuration
  - Error conditions and exceptions

### Testing Approach
- **Integration Tests**: Verify endpoint functionality with real request/response cycles
- **Test Configuration**: Separate test configuration with pytest fixtures
- **Coverage**: Tests cover both successful and error scenarios

### Code Quality
- **Modular Design**: Clear separation of concerns across different layers
- **Error Handling**: Comprehensive exception handling with appropriate HTTP status codes
- **Type Hints**: Full type annotation for better code maintainability
- **Clean Code**: Following Python best practices and PEP 8 standards

## Development Notes

This implementation demonstrates:
- RESTful API design principles
- Clean architecture patterns
- Test-driven development practices
- Production-ready logging and error handling
- Container-based deployment strategya