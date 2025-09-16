from fastapi import FastAPI
from app.api.routes import car_routes, booking_routes

app = FastAPI(
    title="Car Rental API",
    description="A simple REST API for car rental service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(car_routes.router)
app.include_router(booking_routes.router)


@app.get("/")
def root():
    return {
        "message": app.description,
        "status": "active",
        "docs": app.docs_url,
        "redoc": app.redoc_url,
    }